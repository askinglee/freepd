---
title: "PDF 转图片 - 免费在线工具"
date: 2026-01-26
description: "将 PDF 每一页导出为高清 JPG/PNG 图片包。本地转换，支持批量打包下载，隐私绝对安全。"
slug: pdf-to-image
tags: ["PDF工具", "PDF转图片"]
categories: ["在线工具"]
---

## PDF 转图片

{{< rawhtml >}}
<div id="pdf-to-image-tool" class="pdf-tool-container">
    <div class="drop-zone" id="drop-zone">
        <p>拖拽 PDF 文件到这里，或 <span class="browse-btn">点击浏览</span></p>
        <input type="file" id="file-input" accept=".pdf" style="display: none;">
    </div>

    <div id="preview-container" class="preview-grid" style="display: none;">
        <!-- 页面预览将显示在这里 -->
    </div>

    <div class="actions main-actions" style="display: none;" id="tool-actions">
        <button id="download-all-btn" class="primary-btn btn-large">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v4m4-5l5 5 5-5m-5 5V3"/></svg>
            打包下载所有图片 (ZIP)
        </button>
        <button id="clear-btn" class="secondary-btn btn-large">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18m-2 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
            清空
        </button>
    </div>

    <div id="status-msg" class="status-msg"></div>
</div>

<!-- Lightbox Modal -->
<div id="lightbox" class="lightbox-modal">
    <span class="lightbox-close">&times;</span>
    <img class="lightbox-content" id="lightbox-img">
    <div id="lightbox-caption" class="lightbox-caption"></div>
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
.preview-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}
.page-item {
    border: 1px solid #e5e7eb;
    padding: 8px;
    background: #fff;
    border-radius: 8px;
    text-align: center;
    transition: transform 0.2s, box-shadow 0.2s;
    cursor: zoom-in;
}
.page-item:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
.dark .page-item { background: #374151; border-color: #4b5563; }
.page-item canvas {
    max-width: 100%;
    height: auto;
    border-radius: 4px;
    margin-bottom: 8px;
}
.page-label { font-size: 0.875rem; color: #4b5563; font-weight: 500; }
.dark .page-label { color: #d1d5db; }

.main-actions {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid #e5e7eb;
}
.dark .main-actions { border-color: #374151; }

.btn-large {
    padding: 1rem 2rem;
    font-size: 1.125rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    transition: all 0.2s;
}
.primary-btn {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 600;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.39);
}
.primary-btn:hover {
    transform: scale(1.02);
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.45);
}
.secondary-btn {
    background: #fff;
    color: #4b5563;
    border: 2px solid #e5e7eb;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 600;
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
.dark .secondary-btn:hover {
    background: #4b5563;
}

.status-msg { margin-top: 1.5rem; font-size: 1rem; text-align: center; }
.success { color: #059669; font-weight: 500; }
.error { color: #dc2626; font-weight: 500; }

/* Lightbox Styles */
.lightbox-modal {
    display: none;
    position: fixed;
    z-index: 1000;
    padding-top: 50px;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0,0,0,0.9);
}
.lightbox-content {
    margin: auto;
    display: block;
    max-width: 90%;
    max-height: 80vh;
    border-radius: 8px;
    animation-name: zoom;
    animation-duration: 0.3s;
}
@keyframes zoom {
    from {transform:scale(0)} 
    to {transform:scale(1)}
}
.lightbox-close {
    position: absolute;
    top: 15px;
    right: 35px;
    color: #f1f1f1;
    font-size: 40px;
    font-weight: bold;
    transition: 0.3s;
    cursor: pointer;
}
.lightbox-close:hover { color: #bbb; }
.lightbox-caption {
    margin: auto;
    display: block;
    width: 80%;
    max-width: 700px;
    text-align: center;
    color: #ccc;
    padding: 10px 0;
    height: 150px;
}
</style>

<!-- Load pdf.js and JSZip -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>

<script>
    const pdfjsLib = window['pdfjs-dist/build/pdf'];
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const previewContainer = document.getElementById('preview-container');
    const toolActions = document.getElementById('tool-actions');
    const downloadAllBtn = document.getElementById('download-all-btn');
    const clearBtn = document.getElementById('clear-btn');
    const statusMsg = document.getElementById('status-msg');
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxCaption = document.getElementById('lightbox-caption');
    const closeBtn = document.querySelector('.lightbox-close');

    let currentPdf = null;

    dropZone.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', (e) => handleFile(e.target.files[0]));
    
    dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('drag-over'); });
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        handleFile(e.dataTransfer.files[0]);
    });

    async function handleFile(file) {
        if (!file || file.type !== 'application/pdf') return;

        statusMsg.className = 'status-msg';
        statusMsg.innerText = '正在加载 PDF...';
        if (previewContainer) {
            previewContainer.innerHTML = '';
            previewContainer.style.display = 'grid';
        }
        if (toolActions) toolActions.style.display = 'none';

        try {
            const arrayBuffer = await file.arrayBuffer();
            const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
            currentPdf = await loadingTask.promise;

            statusMsg.innerText = `PDF 已加载，共有 ${currentPdf.numPages} 页。正在渲染预览...`;

            for (let i = 1; i <= currentPdf.numPages; i++) {
                const page = await currentPdf.getPage(i);
                const viewport = page.getViewport({ scale: 0.5 }); 
                
                const pageItem = document.createElement('div');
                pageItem.className = 'page-item';
                pageItem.title = '点击查看大图';
                
                const canvas = document.createElement('canvas');
                const context = canvas.getContext('2d');
                canvas.height = viewport.height;
                canvas.width = viewport.width;

                await page.render({ canvasContext: context, viewport: viewport }).promise;
                
                pageItem.appendChild(canvas);
                const label = document.createElement('div');
                label.className = 'page-label';
                label.innerText = `第 ${i} 页`;
                pageItem.appendChild(label);

                // Add click event for lightbox
                pageItem.addEventListener('click', () => openLightbox(i, canvas));

                if (previewContainer) previewContainer.appendChild(pageItem);
            }

            statusMsg.className = 'status-msg success';
            statusMsg.innerText = '✅ 预览完成。';
            if (toolActions) toolActions.style.display = 'flex';
        } catch (error) {
            console.error(error);
            statusMsg.className = 'status-msg error';
            statusMsg.innerText = '❌ 加载失败：' + error.message;
        }
    }

    async function openLightbox(pageNum, thumbCanvas) {
        lightbox.style.display = "block";
        lightboxImg.src = thumbCanvas.toDataURL(); // Show thumb first
        lightboxCaption.innerText = `正在渲染第 ${pageNum} 页的高清预览...`;

        try {
            const page = await currentPdf.getPage(pageNum);
            const viewport = page.getViewport({ scale: 1.5 }); // Higher res for lightbox
            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;

            await page.render({ canvasContext: context, viewport: viewport }).promise;
            lightboxImg.src = canvas.toDataURL('image/png');
            lightboxCaption.innerText = `第 ${pageNum} 页 - 高清预览`;
        } catch (err) {
            console.error(err);
            lightboxCaption.innerText = `无法加载高清预览`;
        }
    }

    closeBtn.onclick = () => lightbox.style.display = "none";
    lightbox.onclick = (e) => {
        if (e.target === lightbox || e.target === closeBtn) {
            lightbox.style.display = "none";
        }
    }

    downloadAllBtn.addEventListener('click', async () => {
        try {
            downloadAllBtn.disabled = true;
            statusMsg.className = 'status-msg';
            statusMsg.innerText = '正在生成高分辨率图片并 ZIP 打包...';

            const zip = new JSZip();
            
            for (let i = 1; i <= currentPdf.numPages; i++) {
                statusMsg.innerText = `正在处理第 ${i}/${currentPdf.numPages} 页...`;
                const page = await currentPdf.getPage(i);
                const viewport = page.getViewport({ scale: 2.0 }); 
                
                const canvas = document.createElement('canvas');
                const context = canvas.getContext('2d');
                canvas.height = viewport.height;
                canvas.width = viewport.width;

                await page.render({ canvasContext: context, viewport: viewport }).promise;
                
                const imageData = canvas.toDataURL('image/png').split(',')[1];
                zip.file(`page_${i}.png`, imageData, { base64: true });
            }

            statusMsg.innerText = '正在生成压缩包，请稍候...';
            const content = await zip.generateAsync({ type: 'blob' });
            
            const link = document.createElement('a');
            link.href = URL.createObjectURL(content);
            link.download = `pdf_images_${new Date().getTime()}.zip`;
            link.click();

            statusMsg.className = 'status-msg success';
            statusMsg.innerText = '✅ 下载已开始。';
        } catch (error) {
            console.error(error);
            statusMsg.className = 'status-msg error';
            statusMsg.innerText = '❌ 制作 ZIP 失败：' + error.message;
        } finally {
            downloadAllBtn.disabled = false;
        }
    });

    clearBtn.addEventListener('click', () => {
        if (previewContainer) {
            previewContainer.innerHTML = '';
            previewContainer.style.display = 'none';
        }
        if (toolActions) toolActions.style.display = 'none';
        statusMsg.innerHTML = '';
        currentPdf = null;
    });
</script>
{{< /rawhtml >}}

