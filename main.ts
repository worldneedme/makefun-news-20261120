// News-image entry (Node 22, standard library only): the image is the
// entry.png beside this file, drawn by draw_news.py, and the program copies
// it to /output/entry.png. The gate takes a whole PNG or JPEG of at most
// 1 MiB and 1024 by 1024 pixels, and the judge sees exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(new URL('./entry.png', import.meta.url), dest);
// The gate refuses an image over 1 MiB; fail loudly instead of entering one.
if (statSync(dest).size > 1048576) throw new Error('entry.png exceeds 1 MiB');
