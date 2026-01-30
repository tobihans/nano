import * as esbuild from "esbuild";

const shouldWatch = process.argv.includes("--watch");

/** @type {esbuild.BuildOptions} */
const config = {
  entryPoints: ["ui/app.ts"],
  bundle: true,
  outdir: "ui/dist",
  format: "esm",
  minify: !shouldWatch,
  sourcemap: shouldWatch,
  target: ["es2020"],
  logLevel: "info",
};

if (shouldWatch) {
  const ctx = await esbuild.context(config);
  await ctx.watch();
  console.log("Watching for changes...");
} else {
  await esbuild.build(config);
}
