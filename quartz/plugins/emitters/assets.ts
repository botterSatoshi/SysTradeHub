import { FilePath, joinSegments, slugifyFilePath } from "../../util/path"
import { QuartzEmitterPlugin } from "../types"
import path from "path"
import fs from "fs"
import { glob } from "../../util/glob"
import { Argv } from "../../util/ctx"
import { QuartzConfig } from "../../cfg"

const filesToCopy = async (argv: Argv, cfg: QuartzConfig) => {
  // glob all non MD files in content folder and copy it over
  const contentFiles = await glob("**", argv.directory, ["**/*.md", ...cfg.configuration.ignorePatterns])
  
  // Also glob all files in root images folder
  const rootImagesPath = path.resolve(path.dirname(argv.directory), "images")
  let imagesFiles: FilePath[] = []
  
  if (fs.existsSync(rootImagesPath)) {
    const imagesGlob = await glob("**", rootImagesPath as FilePath, cfg.configuration.ignorePatterns)
    // Prefix images files with "images/" and normalize path separators
    imagesFiles = imagesGlob.map(fp => path.posix.join("images", fp) as FilePath)
  }
  
  return [...contentFiles, ...imagesFiles]
}

const copyFile = async (argv: Argv, fp: FilePath) => {
  let src: FilePath
  
  // Normalize path separators for consistent comparison
  const normalizedFp = fp.replace(/\\/g, '/')
  
  // Check if this is a file from root images folder
  if (normalizedFp.startsWith("images/")) {
    // For images files, use the root directory instead of argv.directory
    const rootDir = path.dirname(argv.directory)
    src = joinSegments(rootDir, fp) as FilePath
  } else {
    // For content files, use argv.directory as before
    src = joinSegments(argv.directory, fp) as FilePath
  }

  const name = slugifyFilePath(fp)
  const dest = joinSegments(argv.output, name) as FilePath

  // ensure dir exists
  const dir = path.dirname(dest) as FilePath
  await fs.promises.mkdir(dir, { recursive: true })

  await fs.promises.copyFile(src, dest)
  return dest
}

export const Assets: QuartzEmitterPlugin = () => {
  return {
    name: "Assets",
    async *emit({ argv, cfg }) {
      const fps = await filesToCopy(argv, cfg)
      for (const fp of fps) {
        yield copyFile(argv, fp)
      }
    },
    async *partialEmit(ctx, _content, _resources, changeEvents) {
      for (const changeEvent of changeEvents) {
        const ext = path.extname(changeEvent.path)
        if (ext === ".md") continue

        // Check if the change is in the root images folder
        const rootImagesPath = path.resolve(path.dirname(ctx.argv.directory), "images")
        const isRootImageFile = changeEvent.path.startsWith(rootImagesPath)
        
        if (changeEvent.type === "add" || changeEvent.type === "change") {
          if (isRootImageFile) {
            // Convert absolute path to relative path with "images/" prefix
            const relativePath = path.relative(path.dirname(ctx.argv.directory), changeEvent.path) as FilePath
            yield copyFile(ctx.argv, relativePath)
          } else {
            // Handle content folder files as before
            yield copyFile(ctx.argv, changeEvent.path)
          }
        } else if (changeEvent.type === "delete") {
          let filePath: FilePath
          if (isRootImageFile) {
            // Convert absolute path to relative path with "images/" prefix
            filePath = path.relative(path.dirname(ctx.argv.directory), changeEvent.path) as FilePath
          } else {
            filePath = changeEvent.path
          }
          
          const name = slugifyFilePath(filePath)
          const dest = joinSegments(ctx.argv.output, name) as FilePath
          await fs.promises.unlink(dest)
        }
      }
    },
  }
}
