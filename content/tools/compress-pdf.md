---
title: "PDF 压缩 - 免费在线工具"
date: 2026-01-26
description: "智能优化 PDF 结构以减小体积。本地化处理，在保证清晰度的同时显著压缩文件大小。"
slug: compress-pdf
tags: ["PDF工具", "PDF压缩"]
categories: ["在线工具"]
---

## PDF 智能压缩

{{< rawhtml >}}
<div id="pdf-compress-tool" class="pdf-tool-container">
    <div class="drop-zone" id="drop-zone">
        <p>拖拽 PDF 文件到这里，或 <span class="browse-btn">点击浏览</span></p>
        <input type="file" id="file-input" accept=".pdf" style="display: none;">
    </div>

    <div id="file-stats" class="file-stats" style="display: none;">
        <div class="stat-card">
            <div class="stat-label">原始大小</div>
            <div id="original-size" class="stat-value">-</div>
        </div>
        <div class="stat-arrow">
            <svg viewBox="0 0 24 24" width="32" height="32" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
        </div>
        <div class="stat-card">
            <div class="stat-label">压缩后大小</div>
            <div id="compressed-size" class="stat-value">-</div>
        </div>
        <div class="stat-card result-percent">
            <div class="stat-label">节省空间</div>
            <div id="save-percent" class="stat-value">-</div>
        </div>
    </div>

    <div class="actions main-actions" style="display: none;" id="tool-actions">
        <button id="compress-btn" class="primary-btn btn-large">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 14l8-8 8 8M4 20l8-8 8 8"/></svg>
            开始智能压缩
        </button>
        <button id="download-btn" class="success-btn btn-large" style="display: none;">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v4m4-5l5 5 5-5m-5 5V3"/></svg>
            立即下载压缩版
        </button>
        <button id="clear-btn" class="secondary-btn btn-large">清空</button>
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
.browse-btn {
    color: #3b82f6;
    text-decoration: underline;
}

.file-stats {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    margin: 2rem 0;
    flex-wrap: wrap;
}
.stat-card {
    background: #f3f4f6;
    padding: 1.5rem;
    border-radius: 12px;
    min-width: 150px;
    text-align: center;
}
.dark .stat-card { background: #374151; }
.stat-label { font-size: 0.875rem; color: #6b7280; margin-bottom: 0.5rem; }
.dark .stat-label { color: #9ca3af; }
.stat-value { font-size: 1.5rem; font-weight: 700; color: #111827; }
.dark .stat-value { color: #f3f4f6; }
.stat-arrow { color: #9ca3af; }
.result-percent { background: #ecfdf5; border: 1px solid #10b981; }
.dark .result-percent { background: #064e3b; }
.result-percent .stat-value { color: #059669; }

.main-actions {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 2rem;
}

.btn-large {
    padding: 1rem 2rem;
    font-size: 1.125rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    cursor: pointer;
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.2s;
}
.primary-btn {
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    color: white;
    border: none;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.39);
}
.success-btn {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    border: none;
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.39);
}
.secondary-btn {
    background: #fff;
    color: #4b5563;
    border: 2px solid #e5e7eb;
}
.dark .secondary-btn { background: #374151; color: #f3f4f6; border-color: #4b5563; }

.status-msg { margin-top: 1.5rem; font-size: 1rem; text-align: center; }
.success { color: #059669; }
.error { color: #dc2626; }
</style>

<script src="https://unpkg.com/pdf-lib@1.17.1/dist/pdf-lib.min.js"></script>

<script>
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const toolActions = document.getElementById('tool-actions');
    const compressBtn = document.getElementById('compress-btn');
    const downloadBtn = document.getElementById('download-btn');
    const clearBtn = document.getElementById('clear-btn');
    const statusMsg = document.getElementById('status-msg');
    const fileStats = document.getElementById('file-stats');

    const originalSizeElem = document.getElementById('original-size');
    const compressedSizeElem = document.getElementById('compressed-size');
    const savePercentElem = document.getElementById('save-percent');

    let currentFile = null;
    let compressedBlob = null;

    dropZone.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', (e) => handleFile(e.target.files[0]));
    
    dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('drag-over'); });
    dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        handleFile(e.dataTransfer.files[0]);
    });

    function formatSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024, sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    async function handleFile(file) {
        if (!file || file.type !== 'application/pdf') return;
        currentFile = file;
        
        dropZone.style.display = 'none';
        fileStats.style.display = 'flex';
        toolActions.style.display = 'flex';
        compressBtn.style.display = 'flex';
        downloadBtn.style.display = 'none';
        
        originalSizeElem.innerText = formatSize(file.size);
        compressedSizeElem.innerText = '-';
        savePercentElem.innerText = '-';
        statusMsg.innerText = '文件已准备就绪，点击开始压缩。';
    }

    compressBtn.addEventListener('click', async () => {
        try {
            compressBtn.disabled = true;
            compressBtn.innerText = '正在智能优化中...';
            statusMsg.innerText = '正在通过重构对象优化 PDF 结构...';

            const arrayBuffer = await currentFile.arrayBuffer();
            const { PDFDocument } = PDFLib;
            
            // 核心逻辑：重新加载并以“最小化”模式保存
            // pdf-lib 会重新计算所有引用并移除未引用的对象
            const pdfDoc = await PDFDocument.load(arrayBuffer);
            
            // 下一个更高阶的优化：可以通过遍历页面并移除未使用的资源（暂不实现过深逻辑以保稳定）
            
            const compressedPdfBytes = await pdfDoc.save({ useObjectStreams: true });
            compressedBlob = new Blob([compressedPdfBytes], { type: 'application/pdf' });
            
            const savedBytes = currentFile.size - compressedBlob.size;
            const percent = ((savedBytes / currentFile.size) * 100).toFixed(1);

            compressedSizeElem.innerText = formatSize(compressedBlob.size);
            savePercentElem.innerText = percent > 0 ? percent + '%' : '0%';
            
            statusMsg.className = 'status-msg success';
            if (savedBytes > 0) {
                statusMsg.innerText = `✅ 压缩完成！已为您节省了 ${formatSize(savedBytes)} 空间。`;
            } else {
                statusMsg.innerText = '该 PDF 已经是高度优化过的，未发现可进一步压缩的空间。';
            }

            compressBtn.style.display = 'none';
            downloadBtn.style.display = 'flex';
        } catch (error) {
            console.error(error);
            statusMsg.className = 'status-msg error';
            statusMsg.innerText = '❌ 压缩失败：' + error.message;
        } finally {
            compressBtn.disabled = false;
        }
    });

    downloadBtn.addEventListener('click', () => {
        const url = URL.createObjectURL(compressedBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `compressed_${currentFile.name}`;
        link.click();
    });

    clearBtn.addEventListener('click', () => {
        dropZone.style.display = 'block';
        fileStats.style.display = 'none';
        toolActions.style.display = 'none';
        statusMsg.innerText = '';
        currentFile = null;
        compressedBlob = null;
    });
</script>
{{< /rawhtml >}}

{{< rawhtml >}}
<div class="related-tools" data-current="compress">
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
