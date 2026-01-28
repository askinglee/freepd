---
title: "PDF 在线预览 - 免费在线工具"
date: 2026-01-26
description: "免费在线PDF预览工具，无需下载软件，直接在浏览器中快速查看PDF文档。100%本地处理，保护文档隐私。"
slug: pdf-preview
tags: ["PDF工具", "PDF预览"]
keywords:
  - PDF预览
  - PDF在线预览
  - PDF查看器
  - 在线PDF阅读
  - PDF在线打开
  - 免费PDF预览
  - 浏览器PDF查看
  - PDF阅读器
categories: ["在线工具"]
---

## PDF 在线预览

{{< rawhtml >}}
<div id="pdf-preview-tool" class="pdf-tool-container">
    <div class="drop-zone" id="drop-zone">
        <p>拖拽 PDF 文件到这里，或 <span class="browse-btn">点击浏览</span></p>
        <input type="file" id="file-input" accept=".pdf" style="display: none;">
    </div>

    <div id="viewer-controls" class="viewer-controls sticky-top" style="display: none;">
        <div class="control-group">
            <button id="prev-btn" class="secondary-btn">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 18l-6-6 6-6"/></svg>
                上一页
            </button>
            <span class="page-info">第 <span id="page-num">1</span> / <span id="page-count">-</span> 页</span>
            <button id="next-btn" class="secondary-btn">
                下一页
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
            </button>
        </div>
        <div class="control-group">
            <button id="zoom-out" class="secondary-btn" title="缩小">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14"/></svg>
            </button>
            <span id="zoom-percent">100%</span>
            <button id="zoom-in" class="secondary-btn" title="放大">
                <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg>
            </button>
        </div>
        <button id="clear-btn" class="secondary-btn danger-hover">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 18L18 6M6 6l12 12"/></svg>
            关闭
        </button>
    </div>

    <div id="pdf-viewer-container" class="pdf-viewer-container" style="display: none;">
        <button id="floating-prev" class="floating-nav left" title="上一页">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="3"><path d="M15 18l-6-6 6-6"/></svg>
        </button>
        <canvas id="pdf-render"></canvas>
        <button id="floating-next" class="floating-nav right" title="下一页">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="3"><path d="M9 18l6-6-6-6"/></svg>
        </button>
    </div>

    <div id="status-msg" class="status-msg"></div>
</div>

<style>
.pdf-tool-container {
    margin: 2rem 0;
    padding: 2rem;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    background: #ffffff;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.dark .pdf-tool-container {
    background: #1f2937;
    border-color: #374151;
}
.drop-zone {
    border: 3px dashed #d1d5db;
    border-radius: 12px;
    padding: 3rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s;
    background: #f9fafb;
}
.dark .drop-zone {
    background: #111827;
    border-color: #4b5563;
}
.drop-zone.drag-over {
    border-color: #3b82f6;
    background: #eff6ff;
}

.viewer-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid #e5e7eb;
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(8px);
    z-index: 100;
    transition: all 0.3s;
}
.dark .viewer-controls { 
    border-color: #374151; 
    background: rgba(31, 41, 55, 0.9);
}
.sticky-top {
    position: sticky;
    top: 60px; /* Adjust based on your Hugo theme's header height */
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.control-group {
    display: flex;
    align-items: center;
    gap: 1rem;
}
.page-info, #zoom-percent {
    font-weight: 500;
    color: #4b5563;
    font-size: 0.875rem;
}
.dark .page-info, .dark #zoom-percent { color: #d1d5db; }

.pdf-viewer-container {
    position: relative;
    overflow: auto;
    background: #525659;
    padding: 2rem;
    border-radius: 12px;
    display: flex;
    justify-content: center;
    min-height: 500px;
}
#pdf-render {
    box-shadow: 0 0 30px rgba(0,0,0,0.3);
    background: white;
}

/* Floating Navigation */
.floating-nav {
    position: fixed;
    top: 50%;
    transform: translateY(-50%);
    background: rgba(0, 0, 0, 0.3);
    color: white;
    border: none;
    width: 50px;
    height: 50px;
    border-radius: 50%;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s;
    z-index: 90;
}
.floating-nav:hover {
    background: rgba(0, 0, 0, 0.6);
    transform: translateY(-50%) scale(1.1);
}
.floating-nav.left { left: 20px; }
.floating-nav.right { right: 20px; }

.secondary-btn {
    background: #fff;
    color: #4b5563;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    cursor: pointer;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.2s;
}
.dark .secondary-btn {
    background: #374151;
    color: #f3f4f6;
    border-color: #4b5563;
}
.secondary-btn:hover {
    background: #f9fafb;
    border-color: #d1d5db;
}
.secondary-btn.danger-hover:hover {
    color: #ef4444;
    border-color: #fecaca;
    background: #fef2f2;
}

.status-msg { margin-top: 1rem; font-size: 1rem; text-align: center; }
.success { color: #059669; font-weight: 500; }
.error { color: #dc2626; font-weight: 500; }
</style>

<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>

<script>
    const pdfjsLib = window['pdfjs-dist/build/pdf'];
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const viewerControls = document.getElementById('viewer-controls');
    const pdfViewerContainer = document.getElementById('pdf-viewer-container');
    const canvas = document.getElementById('pdf-render');
    const ctx = canvas.getContext('2d');
    const statusMsg = document.getElementById('status-msg');

    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const floatPrev = document.getElementById('floating-prev');
    const floatNext = document.getElementById('floating-next');
    const pageNumElem = document.getElementById('page-num');
    const pageCountElem = document.getElementById('page-count');
    const zoomInBtn = document.getElementById('zoom-in');
    const zoomOutBtn = document.getElementById('zoom-out');
    const zoomPercentElem = document.getElementById('zoom-percent');
    const clearBtn = document.getElementById('clear-btn');

    let pdfDoc = null;
    let pageNum = 1;
    let scale = 1.0;
    let isRendering = false;
    let pageNumPending = null;

    dropZone.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', (e) => handleFile(e.target.files[0]));

    async function handleFile(file) {
        if (!file || file.type !== 'application/pdf') return;

        statusMsg.innerText = '正在加载 PDF...';
        try {
            const arrayBuffer = await file.arrayBuffer();
            pdfDoc = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
            
            pageCountElem.innerText = pdfDoc.numPages;
            pageNum = 1;
            scale = 1.0;
            
            dropZone.style.display = 'none';
            viewerControls.style.display = 'flex';
            pdfViewerContainer.style.display = 'flex';
            statusMsg.innerText = '';

            renderPage(pageNum);
            setupKeyboard();
        } catch (error) {
            console.error(error);
            statusMsg.className = 'status-msg error';
            statusMsg.innerText = '加载失败：' + error.message;
        }
    }

    async function renderPage(num) {
        isRendering = true;
        
        try {
            const page = await pdfDoc.getPage(num);
            const viewport = page.getViewport({ scale });
            canvas.height = viewport.height;
            canvas.width = viewport.width;

            const renderContext = {
                canvasContext: ctx,
                viewport: viewport
            };

            await page.render(renderContext).promise;
            isRendering = false;

            if (pageNumPending !== null) {
                renderPage(pageNumPending);
                pageNumPending = null;
            }

            pageNumElem.innerText = num;
            zoomPercentElem.innerText = `${Math.round(scale * 100)}%`;
            
            // Update button states
            prevBtn.disabled = floatPrev.disabled = (num <= 1);
            nextBtn.disabled = floatNext.disabled = (num >= pdfDoc.numPages);
            floatPrev.style.opacity = (num <= 1) ? "0.3" : "1";
            floatNext.style.opacity = (num >= pdfDoc.numPages) ? "0.3" : "1";
        } catch (error) {
            console.error(error);
            isRendering = false;
        }
    }

    function queueRenderPage(num) {
        if (isRendering) {
            pageNumPending = num;
        } else {
            renderPage(num);
        }
    }

    const goPrev = () => {
        if (pageNum <= 1) return;
        pageNum--;
        queueRenderPage(pageNum);
    };

    const goNext = () => {
        if (!pdfDoc || pageNum >= pdfDoc.numPages) return;
        pageNum++;
        queueRenderPage(pageNum);
    };

    prevBtn.addEventListener('click', goPrev);
    nextBtn.addEventListener('click', goNext);
    floatPrev.addEventListener('click', goPrev);
    floatNext.addEventListener('click', goNext);

    function setupKeyboard() {
        document.addEventListener('keydown', (e) => {
            if (!pdfDoc) return;
            if (e.key === 'ArrowLeft' || e.key === 'PageUp') goPrev();
            if (e.key === 'ArrowRight' || e.key === 'PageDown') goNext();
        });
    }

    zoomInBtn.addEventListener('click', () => {
        scale += 0.2;
        queueRenderPage(pageNum);
    });

    zoomOutBtn.addEventListener('click', () => {
        if (scale <= 0.4) return;
        scale -= 0.2;
        queueRenderPage(pageNum);
    });

    clearBtn.addEventListener('click', () => {
        pdfDoc = null;
        dropZone.style.display = 'block';
        viewerControls.style.display = 'none';
        pdfViewerContainer.style.display = 'none';
        statusMsg.innerText = '';
        fileInput.value = '';
    });
</script>
{{< /rawhtml >}}

{{< rawhtml >}}
<div class="related-tools" data-current="preview">
    <h3>🛠️ 更多 PDF 工具</h3>
    <div class="tool-links">
        <a href="/tools/pdf-preview/" class="tool-link" id="link-preview">
            <span class="icon">👁️</span>
            <div class="info">
                <span class="label">PDF 预览</span>
                <span class="desc">直接在浏览器查看</span>
            </div>
        </a>
        <a href="/tools/merge-pdf/" class="tool-link" id="link-merge">
            <span class="icon">🔗</span>
            <div class="info">
                <span class="label">PDF 合并</span>
                <span class="desc">多个文件合并为一个</span>
            </div>
        </a>
        <a href="/tools/pdf-to-word/" class="tool-link" id="link-to-word">
            <span class="icon">📝</span>
            <div class="info">
                <span class="label">PDF 转 Word <span style="font-size: 10px; color: #ef4444; border: 1px solid #ef4444; padding: 0 2px; border-radius: 4px;">测试</span></span>
                <span class="desc">生成可编辑文字文档</span>
            </div>
        </a>
        <a href="/tools/pdf-to-image/" class="tool-link" id="link-to-image">
            <span class="icon">🖼️</span>
            <div class="info">
                <span class="label">PDF 转图片</span>
                <span class="desc">导出高清无损图片集</span>
            </div>
        </a>
        <a href="/tools/image-to-pdf/" class="tool-link" id="link-to-pdf">
            <span class="icon">📄</span>
            <div class="info">
                <span class="label">图片转 PDF</span>
                <span class="desc">多图一键合成文档</span>
            </div>
        </a>
        <a href="/tools/compress-pdf/" class="tool-link" id="link-compress">
            <span class="icon">📉</span>
            <div class="info">
                <span class="label">PDF 压缩</span>
                <span class="desc">智能优化并减小体积</span>
            </div>
        </a>
    </div>
</div>

<style>
    .related-tools { margin-top: 4rem; padding-top: 2rem; border-top: 2px solid #f3f4f6; }
    .dark .related-tools { border-color: #374151; }
    .related-tools h3 { font-size: 1.25rem; margin-bottom: 1.5rem; color: #374151; }
    .dark .related-tools h3 { color: #d1d5db; }
    .tool-links { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 1rem; }
    .tool-link { display: flex; align-items: center; gap: 0.75rem; padding: 1rem; background: #f9fafb; border: 1px solid #e5e7eb; border-radius: 12px; text-decoration: none !important; transition: all 0.2s; color: #4b5563 !important; }
    .dark .tool-link { background: #374151; border-color: #4b5563; color: #f3f4f6 !important; }
    .tool-link:hover { transform: translateY(-3px); border-color: #3b82f6; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); background: #fff; }
    .dark .tool-link:hover { background: #1f2937; }
    .tool-link .icon { font-size: 1.5rem; }
    .tool-link .info { display: flex; flex-direction: column; gap: 0.25rem; }
    .tool-link .label { font-weight: 700; font-size: 1rem; color: #111827; }
    .dark .tool-link .label { color: #f3f4f6; }
    .tool-link .desc { font-size: 0.8rem; color: #6b7280; font-weight: 400; }
    .dark .tool-link .desc { color: #9ca3af; }
    [data-current="preview"] #link-preview, [data-current="merge"] #link-merge, [data-current="to-image"] #link-to-image, [data-current="to-pdf"] #link-to-pdf, [data-current="compress"] #link-compress, [data-current="to-word"] #link-to-word { display: none; }
</style>
{{< /rawhtml >}}

### 为什么选择我们的工具？

- **隐私安全**：文件不上传服务器，在本地完成处理。
- **完全免费**：无水印，无次数限制。
- **极速处理**：直接在您的浏览器中运行。
