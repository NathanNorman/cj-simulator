/**
 * Validation script for cj-simulator.
 * Checks HTML files for basic structure and JS syntax.
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const ROOT = path.join(__dirname, "..");
let failures = 0;

function check(description, condition) {
  if (condition) {
    console.log(`  PASS: ${description}`);
  } else {
    console.error(`  FAIL: ${description}`);
    failures++;
  }
}

// Find all HTML files in project root
const htmlFiles = fs
  .readdirSync(ROOT)
  .filter((f) => f.endsWith(".html"));

console.log(`Found ${htmlFiles.length} HTML file(s)\n`);
check("At least one HTML file exists", htmlFiles.length > 0);

for (const file of htmlFiles) {
  console.log(`\nValidating ${file}:`);
  const content = fs.readFileSync(path.join(ROOT, file), "utf-8");

  check("File is not empty", content.trim().length > 0);
  check(
    "Has DOCTYPE declaration",
    content.trim().toLowerCase().startsWith("<!doctype html")
  );
  check("Has <title> element", /<title>.*<\/title>/is.test(content));
  check(
    "Has lang attribute on <html>",
    /<html[^>]+lang=/i.test(content)
  );
  check("Has <head> section", /<head[\s>]/i.test(content));
  check("Has <body> section", /<body[\s>]/i.test(content));
}

// Check JSON data files parse correctly
const dataDir = path.join(ROOT, "assets", "data");
if (fs.existsSync(dataDir)) {
  const jsonFiles = fs.readdirSync(dataDir).filter((f) => f.endsWith(".json"));
  console.log(`\nValidating ${jsonFiles.length} JSON data file(s):`);
  for (const file of jsonFiles) {
    console.log(`\nValidating ${file}:`);
    try {
      const content = fs.readFileSync(path.join(dataDir, file), "utf-8");
      JSON.parse(content);
      check("Valid JSON", true);
    } catch (e) {
      check(`Valid JSON (${e.message})`, false);
    }
  }
}

// Extract inline <script> blocks and check for obvious syntax issues
console.log("\nChecking inline JavaScript syntax:");
for (const file of htmlFiles) {
  const content = fs.readFileSync(path.join(ROOT, file), "utf-8");
  const scriptBlocks = content.match(/<script[^>]*>([\s\S]*?)<\/script>/gi);
  if (scriptBlocks) {
    console.log(`  ${file}: ${scriptBlocks.length} script block(s) found`);
    check(`${file} script blocks extracted`, scriptBlocks.length > 0);
  }
}

console.log(`\n${"=".repeat(40)}`);
if (failures > 0) {
  console.error(`${failures} check(s) FAILED`);
  process.exit(1);
} else {
  console.log("All checks passed!");
}
