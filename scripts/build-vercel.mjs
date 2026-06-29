import { cpSync, existsSync, rmSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { resolve } from "node:path";

const root = resolve(fileURLToPath(new URL("..", import.meta.url)));
const source = resolve(root, "site");
const output = resolve(root, "dist");

if (!existsSync(source)) {
  throw new Error("Missing site directory. Nothing to build for Vercel.");
}

rmSync(output, { force: true, recursive: true });
cpSync(source, output, { recursive: true });

console.log("Copied site/ to dist/ for Vercel.");
