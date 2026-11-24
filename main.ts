import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// News image for Tuesday 24 November 2026. The image is drawn by
// draw.py (PIL, procedural art, no network, no photographs) and shipped
// in this repository as entry.png. This entrypoint only copies it to the
// output directory, so every run writes exactly the same bytes.
const HERE = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const src = join(HERE, "entry.png");
// Fail loudly if the shipped asset is not a whole PNG, instead of
// writing a broken file that the sealed gate would reject.
const bytes = readFileSync(src);
const PNG_MAGIC = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);
if (bytes.length < 8 || !bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("entry.png is not a valid PNG");
}
copyFileSync(src, join(outDir, "entry.png"));
console.log(`wrote entry.png (${bytes.length} bytes)`);
