import fs from "fs";
import path from "path";
import process from "process";
import Ajv from "ajv";

const ROOT = process.cwd();
const CONTENT_DIR = path.join(ROOT, "content");
const OUT_DIR = path.join(ROOT, "pages");
const LAYOUT_PATH = path.join(ROOT, "layout", "layout.config.json");
const SCHEMA_PATH = path.join(ROOT, "content", "schema.json");

function readJSON(p) {
  return JSON.parse(fs.readFileSync(p, "utf8"));
}

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll("\"", "&quot;")
    .replaceAll(", 
