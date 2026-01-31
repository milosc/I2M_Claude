---
name: webassembly-module-development
description: Build high-performance WebAssembly modules with WASI 0.3, multi-language support, and production-ready deployments for web, serverless, and AI workloads.
model: sonnet
allowed-tools: Read, Write, Edit, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill webassembly-module-development started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill webassembly-module-development ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill webassembly-module-development instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# WebAssembly Module Development Skill

## What This Skill Enables

Claude can build production-ready WebAssembly modules that run at near-native speeds across web browsers, serverless platforms, and edge computing environments. With WASI 0.3 bringing native async support and WebAssembly 2.0 complete as of March 2025, WASM has transitioned from experimental to production-ready for AI workloads, cloud-native applications, and high-performance web apps.

## Prerequisites

**Required:**
- Claude Pro subscription or Claude Code CLI
- Rust (recommended) or C++/Go compiler
- Node.js 18+ for JavaScript integration
- Basic understanding of systems programming

**What Claude handles automatically:**
- Writing Rust/C++ code optimized for WASM
- Compiling to WebAssembly with proper optimizations
- Generating JavaScript bindings with wasm-bindgen
- Setting up WASI for system calls
- Implementing Component Model for interoperability
- Optimizing binary size and performance
- Testing WASM modules in multiple runtimes

## How to Use This Skill

### Create a Basic WASM Module

**Prompt:** "Build a WebAssembly module in Rust that calculates Fibonacci numbers. Include JavaScript bindings and deploy to npm."

Claude will:
1. Set up Rust project with wasm-pack
2. Write optimized Fibonacci implementation
3. Add wasm-bindgen annotations
4. Compile to WASM with size optimizations
5. Generate TypeScript definitions
6. Create npm package configuration
7. Include usage examples for web and Node.js

### Image Processing with WASM

**Prompt:** "Create a WebAssembly module that applies image filters (grayscale, blur, sharpen) to ImageData from canvas. Optimize for processing 4K images in real-time."

Claude will:
1. Write Rust image processing algorithms
2. Use rayon for parallel processing
3. Interface with JavaScript canvas API
4. Implement zero-copy memory sharing
5. Add SIMD optimizations where available
6. Create worker thread wrapper
7. Benchmark against pure JavaScript

### AI Model Inference with WASM

**Prompt:** "Build a WebAssembly module that runs ONNX neural network models in the browser. Support image classification with MobileNetV3."

Claude will:
1. Integrate wasm-bindgen with onnxruntime-web
2. Load and cache ONNX models
3. Implement preprocessing pipeline
4. Run inference with WebAssembly backend
5. Add batching for multiple inputs
6. Optimize memory allocation
7. Include model quantization for smaller binaries

### Serverless Function with WASI

**Prompt:** "Create a WebAssembly module with WASI 0.3 that processes CSV files, performs data transformations, and writes results to stdout. Deploy to Fermyon Spin."

Claude will:
1. Write Rust code using WASI SDK
2. Implement async file I/O with WASI 0.3
3. Add CSV parsing and transformation logic
4. Configure for Spin serverless platform
5. Set up component model interfaces
6. Add error handling and logging
7. Deploy with spin.toml configuration

## Tips for Best Results

1. **Choose Rust for Production**: While multiple languages compile to WASM, Rust offers the best tooling (wasm-pack, wasm-bindgen) and smallest binary sizes. Ask Claude to use Rust unless you have specific requirements.

2. **Optimize Binary Size**: WASM modules should be <500KB for web deployments. Request `wasm-opt -Oz` optimization and enable LTO (Link-Time Optimization) in Cargo.toml.

3. **Use Component Model**: For WASI 0.3, request Component Model implementation for better interoperability and async support.

4. **Memory Management**: WebAssembly uses linear memory. Ask Claude to implement proper memory allocation strategies and avoid memory leaks with proper drop implementations.

5. **JavaScript Interop**: Use wasm-bindgen for seamless JavaScript integration. Request TypeScript definitions generation for better DX.

6. **SIMD When Available**: For compute-intensive tasks, ask Claude to use WebAssembly SIMD instructions for 4-8x performance improvements.

## Common Workflows

### High-Performance Web App Component
```
"Create a WebAssembly module for my React app that:
1. Parses and validates 10MB JSON files instantly
2. Performs complex data aggregations
3. Exports results to CSV format
4. Includes TypeScript types
5. Loads asynchronously without blocking UI
6. Caches compiled module in IndexedDB
7. Falls back to JavaScript if WASM not supported"
```

### Cryptocurrency Mining (Educational)
```
"Build a WebAssembly SHA-256 hasher in Rust:
1. Implements Bitcoin mining algorithm
2. Uses multi-threading with Web Workers
3. Achieves >1000 hashes per second
4. Includes difficulty adjustment
5. Reports progress to JavaScript
6. Optimized with SIMD instructions"
```

### Video Codec in Browser
```
"Create a WebAssembly H.264 decoder:
1. Decode video streams in real-time (30fps)
2. Output to canvas via ImageData
3. Support seeking and playback controls
4. Use multi-threading for parallel decode
5. Implement memory-efficient frame buffer
6. Package as Web Component"
```

### Database Query Engine
```
"Build a WebAssembly SQLite query engine:
1. Compile SQLite to WASM with WASI
2. Implement virtual file system in browser
3. Support full SQL query syntax
4. Persist database to IndexedDB
5. Include transaction support
6. Expose async API to JavaScript
7. Add query performance analytics"
```

## Troubleshooting

**Issue:** WASM module binary is too large (>2MB)
**Solution:** Enable LTO and opt-level in Cargo.toml, run wasm-opt with -Oz flag, remove unused dependencies, and consider dynamic linking for shared code.

**Issue:** JavaScript can't call WASM functions
**Solution:** Ensure wasm-bindgen attributes are present (#[wasm_bindgen]), rebuild with wasm-pack, and check that JavaScript imports the generated bindings correctly.

**Issue:** Performance slower than expected
**Solution:** Enable WASM SIMD, use multi-threading with Web Workers, avoid frequent boundary crossings between JS and WASM, and profile with Chrome DevTools Performance tab.

**Issue:** Memory errors or crashes
**Solution:** Check for buffer overflows, ensure proper memory allocation, implement Drop trait for cleanup, and use wasm-bindgen's #[wasm_bindgen(inspectable)] for debugging.

**Issue:** WASI functions not available
**Solution:** Update to WASI SDK 0.3+, configure WASI runtime (wasmtime, wasmer), and use preview2 modules. Not all WASI functions are available in browser environments.

**Issue:** Cannot debug WASM code
**Solution:** Enable source maps with wasm-pack build --dev, use Chrome DevTools WASM debugging, add console.log bindings via web_sys crate, or use wasmtime with --invoke for CLI debugging.

## Learn More

- [WebAssembly Official Site](https://webassembly.org/)
- [Rust and WebAssembly Book](https://rustwasm.github.io/book/)
- [wasm-pack Documentation](https://rustwasm.github.io/wasm-pack/)
- [WASI 0.3 Specification](https://github.com/WebAssembly/WASI/blob/main/preview2/README.md)
- [WebAssembly Component Model](https://github.com/WebAssembly/component-model)
- [AssemblyScript Language](https://www.assemblyscript.org/)


## Key Features

- Near-native performance in browser and serverless
- Multi-language support: Rust, C++, Go, AssemblyScript
- WASI 0.3 with native async support
- Component Model for interoperability

## Use Cases

- High-performance web applications
- AI model inference in browser
- Serverless functions with portable code

## Examples

### Example 1: Fibonacci Calculator (Rust)

```rust
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn fibonacci(n: u32) -> u64 {
    match n {
        0 => 0,
        1 => 1,
        _ => {
            let mut a = 0u64;
            let mut b = 1u64;
            for _ in 2..=n {
                let temp = a + b;
                a = b;
                b = temp;
            }
            b
        }
    }
}

#[wasm_bindgen]
pub struct Calculator {
    cache: Vec<u64>,
}

#[wasm_bindgen]
impl Calculator {
    #[wasm_bindgen(constructor)]
    pub fn new() -> Calculator {
        Calculator { cache: vec![0, 1] }
    }

    pub fn nth(&mut self, n: usize) -> u64 {
        while self.cache.len() <= n {
            let len = self.cache.len();
            let next = self.cache[len - 1] + self.cache[len - 2];
            self.cache.push(next);
        }
        self.cache[n]
    }
}
```

### Example 2: Image Grayscale Filter

```rust
use wasm_bindgen::prelude::*;
use wasm_bindgen::Clamped;
use web_sys::ImageData;

#[wasm_bindgen]
pub fn grayscale(data: &mut [u8]) {
    for pixel in data.chunks_exact_mut(4) {
        let gray = (0.299 * pixel[0] as f32
            + 0.587 * pixel[1] as f32
            + 0.114 * pixel[2] as f32) as u8;
        pixel[0] = gray;
        pixel[1] = gray;
        pixel[2] = gray;
    }
}

#[wasm_bindgen]
pub fn process_image(image_data: ImageData) -> Result<ImageData, JsValue> {
    let mut data = image_data.data().to_vec();
    grayscale(&mut data);
    
    ImageData::new_with_u8_clamped_array_and_sh(
        Clamped(&data),
        image_data.width(),
        image_data.height(),
    )
}
```

### Example 3: JavaScript Integration

```javascript
import init, { fibonacci, Calculator } from './pkg/wasm_module.js';

async function runWasm() {
  // Initialize the WASM module
  await init();

  // Call simple function
  console.log('Fibonacci(10):', fibonacci(10));

  // Use class instance
  const calc = new Calculator();
  console.log('nth(20):', calc.nth(20));
  console.log('nth(30):', calc.nth(30));

  // Process image
  const canvas = document.getElementById('canvas');
  const ctx = canvas.getContext('2d');
  const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  
  const processedImage = process_image(imageData);
  ctx.putImageData(processedImage, 0, 0);
}

runWasm();
```

### Example 4: Cargo.toml Configuration

```toml
[package]
name = "wasm-module"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib", "rlib"]

[dependencies]
wasm-bindgen = "0.2"
web-sys = { version = "0.3", features = ["ImageData"] }
js-sys = "0.3"

[profile.release]
opt-level = "z"
lto = true
codegen-units = 1
panic = "abort"

[package.metadata.wasm-pack.profile.release]
wasm-opt = ['-Oz']
```

## Troubleshooting

### wasm-pack build fails

Ensure Rust toolchain is up-to-date (rustup update), wasm32-unknown-unknown target is installed, and Cargo.toml has correct crate-type.

### Binary size too large

Enable LTO, set opt-level = 'z', run wasm-opt -Oz, and remove debug symbols with wasm-strip.

### JavaScript imports fail

Use correct import path to pkg/ directory, ensure init() is called before using WASM functions, and check browser console for loading errors.

## Learn More

For additional documentation and resources, visit:

https://webassembly.org/
