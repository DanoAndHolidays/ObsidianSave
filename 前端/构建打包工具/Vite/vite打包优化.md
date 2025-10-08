## 打包优化
理论：
- 公共库通过cdn来引入，本地会有缓存，有对应的文件指纹。
- 如果分块过多，可能会增加请求数量，所以需要平衡。

1. **代码分割与懒加载**
核心原则
- **路由级分割**：每个路由单独打包
- **组件级分割**：大型组件按需加载
- **第三方库分割**：按使用频率和体积分组

实践示例
```javascript
// 路由懒加载
const Home = () => import('@/views/Home.vue')
const About = () => import('@/views/About.vue')

// 组件懒加载
const HeavyComponent = defineAsyncComponent(() => 
  import('@/components/HeavyComponent.vue')
)
```
2. **第三方依赖优化**
按需引入
```javascript
// ❌ 不推荐 - 全量引入
import _ from 'lodash'

// ✅ 推荐 - 按需引入
import debounce from 'lodash/debounce'
```
CDN 外部化
```javascript
// vite.config.js
export default {
  build: {
    rollupOptions: {
      external: ['vue', 'element-plus'],
      output: {
        globals: {
          vue: 'Vue',
          'element-plus': 'ElementPlus'
        }
      }
    }
  }
}
```

3. **资源优化**
图片优化
图片的优化对前端性能至关重要，原因有几个方面。首先，图片是现代网页中最常见且最占用带宽的资源之一。在大多数网站中，图片的体积通常占据了整个页面资源的很大一部分，尤其是对于内容丰富的页面（如电商网站、博客、新闻网站等）而言。如果不对图片进行优化，加载这些图片会大大拖慢页面的渲染速度，影响用户体验，甚至增加CDN或服务器的负担。

4. **大大降低页面加载时间**： 图片通常是网页上最大且最重的资源之一。未经优化的图片会导致网络请求时间过长，尤其是在带宽有限或移动网络环境下，图片加载可能会成为瓶颈。如果使用压缩或更高效的格式（如WebP、AVIF等），可以显著减少图片文件的大小，进而减少页面加载时间。
5. **提高缓存命中率**： 对图片进行优化后，它们的体积会变小，缓存策略能够更有效地工作。较小的图片资源可以减少浏览器缓存中占用的空间，提高缓存的命中率，从而加快后续访问同一页面时的加载速度。
6. **降低带宽消耗**： 优化图片可以减少传输的数据量，进而减少带宽消耗。对于带宽有限的用户，图片的快速加载和小文件体积是非常重要的，尤其是在移动设备或慢速网络条件下。
7. **提升用户体验**： 网页加载速度直接影响到用户体验。页面加载时间过长可能会导致用户流失。图片优化有助于提升页面的加载速度和响应时间，从而提升用户的浏览体验。

常见的图片类型主要可以分为以下几类：

1. **JPG（JPEG）** ：
    
    - **特点**：一种有损压缩的图片格式，广泛应用于照片类图片。体积较小，支持多种色彩（适用于复杂色彩的图片，如风景照、人物照等）。
    - **优化方式**：通过调整压缩率来减小图片体积。对于需要处理大量照片的场景，使用适当的压缩率可以减小体积，但不牺牲过多的视觉质量。
2. **PNG**：
    
    - **特点**：一种无损压缩的格式，支持透明通道，适用于图标、网页元素、截图等。
    - **优化方式**：对于没有透明通道的PNG图片，建议使用`pngcrush`、`optipng`等工具进行优化，减小无损压缩后的体积。对于透明图片，使用WebP或者AVIF等格式可以替代PNG，进一步降低体积。
3. **GIF**：
    
    - **特点**：常用于制作动画图像。支持多帧动画，但颜色深度有限（最多256种颜色）。文件体积较大。
    - **优化方式**：尽量避免使用GIF动画，尤其是大尺寸的GIF，可以考虑使用WebP或APNG（Animated PNG）作为替代，提供更好的质量和更小的体积。
4. **SVG**：
    
    - **特点**：矢量图格式，适用于简单的图形、图标和标志。可缩放，且不失真。适用于动态、交互式图形。
    - **优化方式**：对SVG文件进行清理，去掉多余的元数据、注释和空格，进一步减小文件体积。可以通过在线工具（如`SVGO`）来优化SVG文件。
5. **WebP**：
    
    - **特点**：支持有损压缩和无损压缩，适用于Web。比JPG、PNG等格式有更高的压缩率，体积更小，支持透明通道。
    - **优化方式**：直接将图片转换为WebP格式，利用其高效压缩算法来减少文件体积，尤其适用于大批量图片的优化。
6. **AVIF**：
    
    - **特点**：一种较新的图片格式，支持高效的有损和无损压缩，支持透明通道，图像质量较高，体积较小。
    - **优化方式**：将图片转换为AVIF格式，能够提供更小的体积和更好的图像质量，尤其适用于图像内容较复杂的场景。

|格式|简介与特性|体积示例（基于图片CDN计算）|发明年份|浏览器兼容性|
|---|---|---|---|---|
|JPG|- 最常见且应用最广泛的图片格式 - 体积适中，通常小于PNG、GIF等格式|158 KB（100%）|1992|几乎所有浏览器支持|
|PNG|- 支持透明通道，可以做部分透明图片 - 体积较大|819 KB（518%）|1996|几乎所有浏览器支持|
|GIF|- 支持动态效果的图片 - 体积较大|423 KB（267%）|1989|几乎所有浏览器支持|
|SVG|- 矢量图，不会因缩放失真 - 本质是标记语言，浏览器可解析渲染 - 体积视内容而定|--|2001|Chrome 4（2010年发布）及以上版本支持 参考资料：caniuse.com/svg|
|WebP|- 支持动态图片 - 压缩效率高，支持有损和无损压缩 - 专为Web平台优化 - 体积较小|136 KB（86%）|2010|Chrome 32（2014年发布）及以上版本支持 参考资料：caniuse.com/webp|
|AVIF|- 支持动态图片 - 压缩率高 - 体积较小|96 KB（60%）|2019|Chrome 85（2020年发布）及以上版本支持 参考资料：caniuse.com/avif|

通过上表可以看出，图片格式大致可分为两类：

- **传统图片格式**：如JPG、PNG、GIF、SVG等，这些格式出现已有二十多年。
- **现代图片格式**：如WebP、AVIF等，这些格式是近十年内新出现的。

从功能和性能上来看：

- **体积**：传统格式的图片文件普遍较大。与JPG格式相比，WebP格式通常可以将文件体积减少约10%，而AVIF格式甚至能减少超过40%的体积。
- **特性**：现代格式支持更多特性，如动态图片和无损压缩等，而传统格式的特性相对单一。
- **浏览器兼容性**：现代格式的浏览器兼容性稍逊一筹，支持它们的浏览器数量相对较少。

如果能够使用WebP、AVIF等现代图片格式，可以显著解决前端应用中图片文件体积大、加载慢、CDN开销高等问题，从而提升性能。

然而，由于浏览器兼容性问题，我们不敢完全依赖这些现代格式，无法大规模应用。

**如何进行图片性能优化？**

- **选择合适的图片格式**：
    
    根据图片的用途选择合适的格式。例如，照片类图片优先使用JPG或WebP，图标和UI元素则使用SVG或WebP。对于需要透明度的图片，优先使用WebP或AVIF。
    
- **使用现代格式与格式回退**：
    尽可能使用WebP和AVIF等现代格式，这些格式提供更高的压缩比和更小的体积，能够显著提升页面加载速度，尤其是在图片数量较多的页面上。
```html
<!-- 现代格式优先，传统格式回退 -->
<picture>
  <!-- AVIF (最高压缩率) -->
  <source srcset="image.avif" type="image/avif">
  
  <!-- WebP (广泛支持) -->
  <source srcset="image.webp" type="image/webp">
  
  <!-- 传统格式 -->
  <source srcset="image.jpg" type="image/jpeg">
  <img src="image.jpg" alt="描述文本" loading="lazy">
</picture>
```
    
- **图片懒加载**：
    这个前面有聊过，图片懒加载是延迟加载图片的技术，只有当图片即将进入视口时才会加载，从而减少初始页面加载的资源消耗，提高页面响应速度。
    
- **使用CDN**：
    将图片托管到CDN（内容分发网络）上，使得图片能够从离用户最近的服务器加载，减少网络延迟，提高加载速度。 各大云服务供应商都提供了图片CDN服务，除了基本的资源存储功能外，还附加了多种强大功能，例如：
    
    - **格式转换与体积压缩**
        原始图片URL：[cdn.example.com/image.jpg](https://link.juejin.cn?target=https%3A%2F%2Fcdn.example.com%2Fimage.jpg "https://cdn.example.com/image.jpg")
        转换为WebP格式并压缩：[cdn.example.com/image.jpg?f…](https://link.juejin.cn?target=https%3A%2F%2Fcdn.example.com%2Fimage.jpg%3Fformat%3Dwebp%26quality%3D80 "https://cdn.example.com/image.jpg?format=webp&quality=80")
        _作用是将JPG格式转换为WebP，同时降低图片质量至80%，减少体积，提高加载速度。_
        
    - **图片尺寸缩放**
        原始图片（原尺寸）： [cdn.example.com/image.jpg](https://link.juejin.cn?target=https%3A%2F%2Fcdn.example.com%2Fimage.jpg "https://cdn.example.com/image.jpg")
        缩放至宽度300px，高度自动适配： [cdn.example.com/image.jpg?w…](https://link.juejin.cn?target=https%3A%2F%2Fcdn.example.com%2Fimage.jpg%3Fwidth%3D300 "https://cdn.example.com/image.jpg?width=300")
        
    - **添加水印**
        原始图片：[cdn.example.com/image.jpg](https://link.juejin.cn?target=https%3A%2F%2Fcdn.example.com%2Fimage.jpg "https://cdn.example.com/image.jpg")
        添加水印（水印文本“Sample”）：[cdn.example.com/image.jpg?w…](https://link.juejin.cn?target=https%3A%2F%2Fcdn.example.com%2Fimage.jpg%3Fwatermark%3Dtext%3ASample%2Copacity%3A50 "https://cdn.example.com/image.jpg?watermark=text:Sample,opacity:50")  
    
    这些功能极大地简化了图片处理的流程，前端无需额外编写代码或使用第三方工具，即可按需动态调整图片，优化网站性能。
    
    我们还可以封装一个图片组件，来根据不同入参获取不同质量和兼容性的图片。
    
- **自动化优化工具**：
    使用构建工具和图片处理工具自动化优化图片。例如，使用`image-webpack-loader`、`sharp`等工具，在Webpack构建过程中自动压缩和转换图片格式。
    
- **图像精灵**：
    将多个小图片（如图标）合并成一张大的图片，使用CSS定位来显示不同的部分，减少HTTP请求次数（减少资源加载时间）。
    
- **将较小的图片转为base64格式内联**：
```javascript
// 使用现代格式
<img src="image.webp" alt="示例">
<picture>
  <source srcset="image.webp" type="image/webp">
  <source srcset="image.jpg" type="image/jpeg">
  <img src="image.jpg" alt="示例">
</picture>
```
字体优化
```javascript
// 只加载需要的字符集
@font-face {
  font-family: 'CustomFont';
  src: url('font.woff2') format('woff2');
  unicode-range: U+000-5FF; /* 拉丁字符 */
  font-display: swap; /* 避免阻塞渲染 */
}
```

4. **构建配置优化**
分块策略
```javascript
// vite.config.js
export default {
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          // 核心框架
          'vue-core': ['vue', 'vue-router', 'pinia'],
          // UI 库
          'ui-library': ['element-plus'],
          // 工具库
          'utils': ['lodash-es', 'axios', 'dayjs'],
          // 业务代码按页面分组
          'home': ['src/views/Home.vue'],
          'about': ['src/views/About.vue']
        }
      }
    }
  }
}
```
Tree Shaking 优化
```javascript
// package.json - 标记副作用
{
  "sideEffects": [
    "*.css",
    "*.scss",
    "**/*/style/*"
  ]
}
```

5. **开发与生产环境差异化**
环境特定配置
```javascript
// vite.config.js
export default defineConfig(({ mode }) => {
  const isProduction = mode === 'production'
  
  return {
    // 生产环境启用压缩
    build: {
      minify: isProduction ? 'terser' : false,
      sourcemap: !isProduction
    },
    
    // 开发环境专用插件
    plugins: [
      !isProduction && visualizer()
    ].filter(Boolean)
  }
})
```

6. **性能监控与分析**
 打包分析
```javascript
// 定期分析打包结果
import { visualizer } from 'rollup-plugin-visualizer'

export default {
  plugins: [
    process.env.ANALYZE && visualizer({
      filename: 'bundle-analysis.html',
      open: true
    })
  ]
}
```

 性能预算
```javascript
// 设置性能阈值
export default {
  build: {
    rollupOptions: {
      output: {
        // 警告大文件
        chunkFileNames: 'assets/[name]-[hash].js',
        manualChunks: {
          vendor: {
            enforce: true,
            minSize: 10000, // 10KB
            maxSize: 250000 // 250KB
          }
        }
      }
    }
  }
}
```

7. **缓存策略**
文件哈希（文件指纹）
```javascript
// 利用浏览器缓存
export default {
  build: {
    rollupOptions: {
      output: {
        // 内容变化时哈希才变化
        chunkFileNames: 'assets/[name]-[hash].js',
        entryFileNames: 'assets/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]'
      }
    }
  }
}
```

8. **压缩与优化**
代码压缩
```javascript
export default {
  build: {
    terserOptions: {
      compress: {
        drop_console: true,    // 移除 console
        drop_debugger: true    // 移除 debugger
      }
    },
    
    // Brotli 压缩（需要插件）
    brotliSize: true
  }
}
```

9. **现代化构建目标**
```javascript
export default {
  build: {
    target: 'es2020', // 根据用户浏览器调整
    // 或者使用 browserslist
    polyfill: false   // 现代浏览器不需要 polyfill
  }
}
```

1. **代码分割（Code Splitting）**：
    - 使用动态导入（import()）来分割代码，实现按需加载。
    - 利用Vue Router的懒加载特性，将不同路由对应的组件分割成不同的代码块。
    - 使用Webpack的SplitChunks或Vite的manualChunks将公共依赖提取到单独 chunk。

2. **Tree Shaking**：
    - 确保使用ES6模块语法（import/export），以便构建工具可以消除未使用的代码。
    - 避免使用具有副作用的模块（例如，在模块顶层执行函数或修改全局变量）。
    - 在package.json中设置"sideEffects"属性，标记无副作用的文件。
        
3. **依赖优化**：
    - 使用CDN引入大型库（如video.js、element-plus等），减少打包体积。
    - 对于必须打包的依赖，选择轻量级替代品（如用dayjs代替moment）。
    - 按需引入组件库（如Element Plus的按需导入）。
        
4. **资源压缩与优化**：
    - 压缩JavaScript、CSS和HTML文件。
    - 使用图像压缩工具（如imagemin）优化图片，并考虑使用现代格式（WebP）。
    - 使用字体子集化，减少字体文件大小。
        
5. **利用浏览器缓存**：
    - 为静态资源设置长期缓存（例如，通过文件名哈希实现）。
    - 将不经常变化的库拆分成单独的chunk，利用缓存。

6. **构建分析**：
    - 使用分析工具（如Webpack Bundle Analyzer、Vite的rollup-plugin-visualizer）分析打包结果，找出体积过大的模块。
    - 根据分析结果进行针对性优化。
        
7. **开发与生产环境的差异化配置**：
    - 开发环境注重调试和热更新，生产环境注重代码压缩和优化。
    - 在生产环境中移除console.log、debugger等调试代码。
        
8. **使用现代JavaScript和CSS**：
    - 使用ES6+语法，并通过Babel等工具转译以兼容目标浏览器。
    - 使用PostCSS和Autoprefixer自动添加CSS前缀。
        
9. **服务端优化**：
    - 开启Gzip或Brotli压缩。
    - 使用HTTP/2。
        
10. **监控与持续优化**：
    - 持续监控打包体积和加载性能。
    - 使用性能预算（performance budget）来设定可接受的资源大小阈值。

## 个人实践
一刻短剧项目的一次打包结果
```bash
PS G:\Save\Grogramming\Vue3\yike> npm run build

> yike@0.0.0 build
> vite build

vite v7.1.6 building for production...
✓ 1645 modules transformed.
dist/index.html                             1.00 kB │ gzip:   0.52 kB
dist/assets/icon-zR7YAv7b.png               5.18 kB
dist/assets/avater_weixin-C4iPkpS4.jpg     14.06 kB
dist/assets/avater-DJtw_nxm.jpg            22.56 kB
dist/assets/avater_jungle-Bs4RDHT7.jpg     34.01 kB
dist/assets/avater_cat-HovCB-jK.jpg        42.89 kB
dist/assets/bg-Ds13Oz8b.jpg                56.52 kB
dist/assets/avater_gebi-2s7w_hoP.jpg      127.84 kB
dist/assets/avater_junhe-DwWDvfFe.jpg     383.24 kB
dist/assets/avater_ji-DoZre7CM.jpg        746.42 kB
dist/assets/avater_sister-ClxQgNX_.jpg  1,652.40 kB
dist/assets/index-BZ1GMPAk.css              0.59 kB │ gzip:   0.32 kB
dist/assets/index-cshfLizc.css              0.67 kB │ gzip:   0.40 kB
dist/assets/index-Cdisn94w.css              0.87 kB │ gzip:   0.48 kB
dist/assets/index-pavrX4tv.css              4.37 kB │ gzip:   1.12 kB
dist/assets/index-CisV2Q7O.css              4.80 kB │ gzip:   0.98 kB
dist/assets/Video-BhTswvAH.css             52.62 kB │ gzip:  13.77 kB
dist/assets/index-Dxnu5WIt.css            353.63 kB │ gzip:  49.07 kB
dist/assets/message-DT946EwC.js             0.13 kB │ gzip:   0.14 kB
dist/assets/play-CsJ9hSnW.js                0.47 kB │ gzip:   0.25 kB
dist/assets/CategoryCard-Dw1Rxoq9.js        0.75 kB │ gzip:   0.46 kB
dist/assets/index-DXo8SZCa.js               1.06 kB │ gzip:   0.61 kB
dist/assets/useDramaInfo-BW8-7f5s.js        1.07 kB │ gzip:   0.50 kB
dist/assets/index-CXFEEZdV.js               1.31 kB │ gzip:   0.75 kB
dist/assets/Page-CCzSuhPF.js                1.73 kB │ gzip:   1.02 kB
dist/assets/index-C2jTH-OF.js               1.84 kB │ gzip:   1.00 kB
dist/assets/index-CAp7QJux.js               2.17 kB │ gzip:   1.22 kB
dist/assets/useDramaStore-BkGkvZ-n.js       2.46 kB │ gzip:   0.92 kB
dist/assets/index-njAX2oa6.js               4.90 kB │ gzip:   1.90 kB
dist/assets/index-Ctmz69-k.js               6.98 kB │ gzip:   2.19 kB
dist/assets/Video-BBrupKNw.js             783.54 kB │ gzip: 239.98 kB
dist/assets/index-Df8JKgGo.js           1,175.45 kB │ gzip: 380.44 kB

(!) Some chunks are larger than 500 kB after minification. Consider:
- Using dynamic import() to code-split the application
- Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
- Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
✓ built in 7.72s
```

*(!) Some chunks are larger than 500 kB after minification. Consider:*
- *Using dynamic import() to code-split the application*
- *Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks*
- *Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.、*

*(!) 一些代码块在压缩后大于 500 KB。考虑以下建议：*
- *使用动态导入 (`import()`) 来进行代码分割*
- *使用 `build.rollupOptions.output.manualChunks` 来改善代码分割：https://rollupjs.org/configuration-options/#output-manualchunks*
- *通过 `build.chunkSizeWarningLimit` 调整此警告的块大小限制*

可以看到有两个包巨大无比：
```bash
dist/assets/Video-BBrupKNw.js             783.54 kB │ gzip: 239.98 kB
dist/assets/index-Df8JKgGo.js           1,175.45 kB │ gzip: 380.44 kB
```

配置manualChunks：
```js
build: {
        target: 'es2020',
        rollupOptions: {
            output: {
                manualChunks(id) {
                    if (id.includes('node_modules')) {
                        return 'vender'
                        // 遍历用到的包，具有node_modules就为第三方库，将这些库统一打包到一起
                    }
                },
            },
        },
    },
```

打包结果：结果就是项目使用的第三方库导致了如此巨大的包。我认为是ELementPlus的全部引入导致的问题。我们可以去每个vue组件中去寻找使用的ui组件，但是这似乎是不太合理
```bash
PS G:\Save\Grogramming\Vue3\yike> npm run build

> yike@0.0.0 build
> vite build

vite v7.1.6 building for production...
✓ 1645 modules transformed.
dist/index.html                             1.09 kB │ gzip:   0.55 kB
dist/assets/icon-zR7YAv7b.png               5.18 kB
dist/assets/avater_weixin-C4iPkpS4.jpg     14.06 kB
dist/assets/avater-DJtw_nxm.jpg            22.56 kB
dist/assets/avater_jungle-Bs4RDHT7.jpg     34.01 kB
dist/assets/avater_cat-HovCB-jK.jpg        42.89 kB
dist/assets/bg-Ds13Oz8b.jpg                56.52 kB
dist/assets/avater_gebi-2s7w_hoP.jpg      127.84 kB
dist/assets/avater_junhe-DwWDvfFe.jpg     383.24 kB
dist/assets/avater_ji-DoZre7CM.jpg        746.42 kB
dist/assets/avater_sister-ClxQgNX_.jpg  1,652.40 kB
dist/assets/index-BZ1GMPAk.css              0.59 kB │ gzip:   0.32 kB
dist/assets/index-cshfLizc.css              0.67 kB │ gzip:   0.40 kB
dist/assets/index-Cdisn94w.css              0.87 kB │ gzip:   0.48 kB
dist/assets/index-pavrX4tv.css              4.37 kB │ gzip:   1.12 kB
dist/assets/index-CisV2Q7O.css              4.80 kB │ gzip:   0.98 kB
dist/assets/Video-BhTswvAH.css             52.62 kB │ gzip:  13.77 kB
dist/assets/index-Dxnu5WIt.css            353.63 kB │ gzip:  49.07 kB
dist/assets/message-BPRgelbg.js             0.13 kB │ gzip:   0.14 kB
dist/assets/play-CBOeR0XM.js                0.47 kB │ gzip:   0.25 kB
dist/assets/CategoryCard-QG2WU9js.js        0.80 kB │ gzip:   0.49 kB
dist/assets/index-CeCMDpoO.js               1.10 kB │ gzip:   0.62 kB
dist/assets/useDramaInfo-L5XOSbK5.js        1.10 kB │ gzip:   0.52 kB
dist/assets/index-DoF5LfHF.js               1.35 kB │ gzip:   0.77 kB
dist/assets/Page-DOBDFDA6.js                1.77 kB │ gzip:   1.04 kB
dist/assets/index-CnF-ihcx.js               1.88 kB │ gzip:   1.02 kB
dist/assets/index-ssAZdXbS.js               2.20 kB │ gzip:   1.23 kB
dist/assets/useDramaStore-CFqwSudb.js       2.51 kB │ gzip:   0.94 kB
dist/assets/index-DhkG06gc.js               4.95 kB │ gzip:   1.92 kB
dist/assets/index-CdQBReCS.js               7.03 kB │ gzip:   2.21 kB
dist/assets/vue-package-C_scTBaz.js        80.04 kB │ gzip:  31.72 kB
dist/assets/Video-BiyQ4AbM.js             783.58 kB │ gzip: 240.00 kB
dist/assets/index-BnagaTIC.js           1,094.59 kB │ gzip: 349.32 kB

(!) Some chunks are larger than 500 kB after minification. Consider:
- Using dynamic import() to code-split the application
- Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
- Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
✓ built in 7.54s
PS G:\Save\Grogramming\Vue3\yike> npm run build

> yike@0.0.0 build
> vite build

vite v7.1.6 building for production...
✓ 1645 modules transformed.
dist/index.html                             1.16 kB │ gzip:   0.56 kB
dist/assets/icon-zR7YAv7b.png               5.18 kB
dist/assets/avater_weixin-C4iPkpS4.jpg     14.06 kB
dist/assets/avater-DJtw_nxm.jpg            22.56 kB
dist/assets/avater_jungle-Bs4RDHT7.jpg     34.01 kB
dist/assets/avater_cat-HovCB-jK.jpg        42.89 kB
dist/assets/bg-Ds13Oz8b.jpg                56.52 kB
dist/assets/avater_gebi-2s7w_hoP.jpg      127.84 kB
dist/assets/avater_junhe-DwWDvfFe.jpg     383.24 kB
dist/assets/avater_ji-DoZre7CM.jpg        746.42 kB
dist/assets/avater_sister-ClxQgNX_.jpg  1,652.40 kB
dist/assets/index-BZ1GMPAk.css              0.59 kB │ gzip:   0.32 kB
dist/assets/index-cshfLizc.css              0.67 kB │ gzip:   0.40 kB
dist/assets/index-Cdisn94w.css              0.87 kB │ gzip:   0.48 kB
dist/assets/index-pavrX4tv.css              4.37 kB │ gzip:   1.12 kB
dist/assets/index-CisV2Q7O.css              4.80 kB │ gzip:   0.98 kB
dist/assets/Video-DWxyu4wm.css              5.76 kB │ gzip:   1.54 kB
dist/assets/index-DmmA6khE.css             12.14 kB │ gzip:   2.63 kB
dist/assets/vender-Vm14vOVl.css           388.38 kB │ gzip:  59.29 kB
dist/assets/message-C-atq9uK.js             0.13 kB │ gzip:   0.14 kB
dist/assets/play-1QTL3lk5.js                0.47 kB │ gzip:   0.25 kB
dist/assets/CategoryCard-C3QnOO87.js        0.78 kB │ gzip:   0.48 kB
dist/assets/useDramaInfo-p5MJ9xJR.js        1.07 kB │ gzip:   0.50 kB
dist/assets/index-D7MMDZDb.js               1.09 kB │ gzip:   0.62 kB
dist/assets/index-XXbDT288.js               1.33 kB │ gzip:   0.76 kB
dist/assets/Page-DWBQCVZ6.js                1.76 kB │ gzip:   1.03 kB
dist/assets/index-TE2xH1-q.js               1.87 kB │ gzip:   1.01 kB
dist/assets/index-DtTop8HW.js               2.19 kB │ gzip:   1.24 kB
dist/assets/useDramaStore-DnmkkFFI.js       2.47 kB │ gzip:   0.93 kB
dist/assets/index-cGLKHZIW.js               4.94 kB │ gzip:   1.91 kB
dist/assets/index-ehwKRs3b.js               6.49 kB │ gzip:   2.99 kB
dist/assets/index-DTkbdbad.js               7.01 kB │ gzip:   2.20 kB
dist/assets/Video-ChevXnao.js              13.23 kB │ gzip:   5.15 kB
dist/assets/vender-DWbTSN4K.js          1,949.23 kB │ gzip: 614.29 kB

(!) Some chunks are larger than 500 kB after minification. Consider:
- Using dynamic import() to code-split the application
- Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
- Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
✓ built in 8.55s
PS G:\Save\Grogramming\Vue3\yike> 
```

我将elementplus单独分包出来：可以看到第三方库全部加起来中的1/3是饿了么，还有大量的icon图标，最开始使用全部导入的决定就是一个错误，我拉了一坨大的在项目里
```bash
dist/assets/element-package-CaNP1MvM.js     894.65 kB │ gzip: 273.16 kB
dist/assets/vender-BySqRoPJ.js            1,046.73 kB │ gzip: 338.76 kB
```

使用插件rollup-plugin-visualizer分析打包结果，其中lodash、video.js与ElementPlus所占的空间最多，

![[Pasted image 20251008190112.png]]

通过饿了么自动导入，lodash部分引入，手动导入图标与仅导入Video.js核心：
```html
<Clock /><FullScreen /><CaretBottom /><More /><Search /><Pointer /><User /><Menu /><Paperclip /><Wallet /><ShoppingCart /><Notebook /><CameraFilled />
<!--这里应该使用自动导入，但是我配置不成功，就只能采用手动逐个导入...以后我不用这个饿了么图标了🥲-->
```

```js
import videojs from 'video.js/core.es.js';
import 'video.js/dist/video-js.css'

import { debounce } from 'lodash-es'
```

```shell
PS G:\Save\Grogramming\Vue3\yike> npm run build:analyze

> yike@0.0.0 build:analyze
> vite build --mode analyze

当前开发模式： analyze
vite v7.1.9 building for analyze...
✓ 1578 modules transformed.
dist/assets/icon-zR7YAv7b.png                   0.47 kB
dist/index.html                                 1.81 kB │ gzip:   0.72 kB
dist/assets/avater-DJtw_nxm.jpg                 2.12 kB
dist/assets/bg-Ds13Oz8b.jpg                    11.67 kB
dist/assets/avater_junhe-bDLUIwvI.webp         17.59 kB
dist/assets/avater_ji-CulGzS0z.webp            22.12 kB
dist/assets/avater_sister-EG9VXyg1.webp        40.19 kB
dist/assets/avater_gebi-D1-GHdH-.webp          40.25 kB
dist/stats.html                             1,021.13 kB │ gzip: 116.85 kB
dist/assets/index-BZ1GMPAk.css                  0.59 kB │ gzip:   0.32 kB
dist/assets/index-cshfLizc.css                  0.67 kB │ gzip:   0.40 kB
dist/assets/index-D1BtapOu.css                  0.90 kB │ gzip:   0.48 kB
dist/assets/index-pavrX4tv.css                  4.37 kB │ gzip:   1.12 kB
dist/assets/index-D-VbuxhM.css                  4.80 kB │ gzip:   0.99 kB
dist/assets/Video-BNK7P4i1.css                  5.76 kB │ gzip:   1.54 kB
dist/assets/index-CFMgteSW.css                 12.18 kB │ gzip:   2.63 kB
dist/assets/element-core-BYwOOVMN.css          26.66 kB │ gzip:   4.69 kB
dist/assets/message-C0jGIuzQ.js                 0.14 kB │ gzip:   0.15 kB
dist/assets/play-er5xd5JJ.js                    0.47 kB │ gzip:   0.25 kB
dist/assets/CategoryCard-vKqGURIo.js            0.78 kB │ gzip:   0.48 kB
dist/assets/useDramaInfo-TYOlYWlc.js            1.11 kB │ gzip:   0.53 kB
dist/assets/index-C4xJit93.js                   1.35 kB │ gzip:   0.74 kB
dist/assets/index-B5yvrhrR.js                   1.60 kB │ gzip:   0.88 kB
dist/assets/Page-BADQaltE.js                    1.81 kB │ gzip:   1.05 kB
dist/assets/index-DThusuqW.js                   2.01 kB │ gzip:   1.09 kB
dist/assets/index-QDFXY1GY.js                   2.45 kB │ gzip:   1.35 kB
dist/assets/useDramaStore-Cgg94Uid.js           2.51 kB │ gzip:   0.95 kB
dist/assets/element-core-BiYJtFnd.js            3.45 kB │ gzip:   1.51 kB
dist/assets/vendor-other-BTrOqZDZ.js            3.61 kB │ gzip:   1.61 kB
dist/assets/index-Duul6NdU.js                   5.17 kB │ gzip:   2.05 kB
dist/assets/index-DCnPn4Ox.js                   7.26 kB │ gzip:   2.34 kB
dist/assets/element-utils-D4GGykBd.js           8.71 kB │ gzip:   4.09 kB
dist/assets/index-CR1mCED1.js                  14.20 kB │ gzip:   8.03 kB
dist/assets/lodash-utils-Ck2_itEy.js           17.57 kB │ gzip:   6.35 kB
dist/assets/vue-ecosystem-CoKluZm0.js          27.17 kB │ gzip:  11.18 kB
dist/assets/element-components-C848VpBO.js     33.57 kB │ gzip:  12.54 kB
dist/assets/axios-http-ngrFHoWO.js             36.01 kB │ gzip:  14.56 kB
dist/assets/Video-ColhTa6L.js                  59.86 kB │ gzip:  41.23 kB
dist/assets/vue-chunks-X15gNV_l.js             90.75 kB │ gzip:  34.98 kB
✓ built in 4.28s

✨ [vite-plugin-imagemin]- compressed image resource successfully:
dist/assets/avater-DJtw_nxm.jpg  -91%  22.04kb / tiny: 2.07kb
dist/assets/bg-Ds13Oz8b.jpg      -80%  55.19kb / tiny: 11.40kb
dist/assets/icon-zR7YAv7b.png    -91%  5.05kb / tiny: 0.46kb
```

![[Pasted image 20251008235818.png]]
最后的打包结果还算满意，但是vite-plugin-imagemin有BUG不能压缩webp，也可能是兼容问题。