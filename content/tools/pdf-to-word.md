---
title: "PDF 转 Word - 免费在线工具"
date: 2026-01-26
description: "【测试中心】基于前端技术实现的 PDF 转 Word 工具。当前支持文字提取保持，暂不支持复杂排版还原。100% 隐私安全。"
slug: pdf-to-word
tags: ["PDF工具", "PDF转Word", "PDF转DOCX", "PDF转Word在线工具", "PDF转Word免费工具", "PDF转Word无需上传", "PDF转Word隐私安全", "PDF转Word本地转换"]
categories: ["在线工具"]
---

## PDF 转 Word

{{< rawhtml >}}
<div id="pdf-to-word-tool" class="pdf-tool-container">
    <div class="drop-zone" id="drop-zone">
        <p>拖拽 PDF 文件到这里，或 <span class="browse-btn">点击浏览</span></p>
        <input type="file" id="file-input" accept=".pdf" style="display: none;">
    </div>

    <div id="file-info" class="file-info-box" style="display: none;">
        <span class="file-icon">📄</span>
        <span id="target-file-name" class="file-name">-</span>
    </div>

    <div class="actions main-actions" style="display: none;" id="tool-actions">
        <button id="convert-btn" class="primary-btn btn-large">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
            立即转换为 Word (DOCX)
        </button>
        <button id="clear-btn" class="secondary-btn btn-large">清空</button>
    </div>

    <div id="status-msg" class="status-msg"></div>

    <div class="test-warning" style="margin-top: 2rem; padding: 1rem; background: #fff7ed; border: 1px solid #fdba74; border-radius: 8px; color: #9a3412; font-size: 0.9rem;">
        <strong>⚠️ 功能测试中：</strong> 目前仅支持提取 PDF 中的<strong>文字内容</strong>并保持基本顺序。暂不支持图片提取、复杂表格布局维护以及艺术字体样式的 1:1 还原。
    </div>
</div>

<style>
.pdf-tool-container { margin: 2rem 0; padding: 2rem; border: 1px solid #e5e7eb; border-radius: 16px; background: #ffffff; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
.dark .pdf-tool-container { background: #1f2937; border-color: #374151; }
.drop-zone { border: 3px dashed #d1d5db; border-radius: 12px; padding: 3rem; text-align: center; cursor: pointer; transition: all 0.3s; background: #f9fafb; }
.dark .drop-zone { background: #111827; border-color: #4b5563; }
.drop-zone.drag-over { border-color: #3b82f6; background: #eff6ff; }
.file-info-box { display: flex; align-items: center; justify-content: center; gap: 10px; margin: 20px 0; padding: 15px; background: #f3f4f6; border-radius: 8px; }
.dark .file-info-box { background: #374151; }
.main-actions { display: flex; justify-content: center; gap: 1rem; margin-top: 2rem; }
.btn-large { padding: 1rem 2rem; font-size: 1.125rem; display: flex; align-items: center; gap: 0.75rem; cursor: pointer; border-radius: 10px; font-weight: 600; transition: all 0.2s; }
.primary-btn { background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%); color: white; border: none; box-shadow: 0 4px 14px rgba(30, 64, 175, 0.39); }
.secondary-btn { background: #fff; color: #4b5563; border: 2px solid #e5e7eb; }
.status-msg { margin-top: 1.5rem; font-size: 1rem; text-align: center; }
.success { color: #059669; }
.error { color: #dc2626; }
</style>

<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/docx@7.1.0/build/index.js"></script>

<script>
    const pdfjsLib = window['pdfjs-dist/build/pdf'];
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
    
    // docs v7.x 使用 window.docx
    function getDocx() {
        return window.docx;
    }

    let currentFile = null;

    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.getElementById('file-info');
    const fileNameDisplay = document.getElementById('target-file-name');
    const toolActions = document.getElementById('tool-actions');
    const convertBtn = document.getElementById('convert-btn');
    const clearBtn = document.getElementById('clear-btn');
    const statusMsg = document.getElementById('status-msg');

    dropZone.onclick = () => fileInput.click();
    fileInput.onchange = (e) => handleFile(e.target.files[0]);
    dropZone.ondragover = (e) => { e.preventDefault(); dropZone.classList.add('drag-over'); };
    dropZone.ondragleave = () => dropZone.classList.remove('drag-over');
    dropZone.ondrop = (e) => { e.preventDefault(); dropZone.classList.remove('drag-over'); handleFile(e.dataTransfer.files[0]); };

    function handleFile(file) {
        if (!file || file.type !== 'application/pdf') return;
        currentFile = file;
        dropZone.style.display = 'none';
        fileInfo.style.display = 'flex';
        fileNameDisplay.innerText = file.name;
        toolActions.style.display = 'flex';
        statusMsg.innerText = '';
    }

    convertBtn.onclick = async () => {
        const docxLib = getDocx();
        if (!docxLib) {
            statusMsg.className = 'status-msg error';
            statusMsg.innerText = '❌ 转换引擎 (docx) 加载失败，请检查网络或刷新重试。';
            return;
        }

        try {
            convertBtn.disabled = true;
            convertBtn.innerText = '正在提取文字...';
            statusMsg.className = 'status-msg';
            statusMsg.innerText = '正在读取 PDF 并提取文本内容...';

            const arrayBuffer = await currentFile.arrayBuffer();
            const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
            
            const docChildren = [];
            
            for (let i = 1; i <= pdf.numPages; i++) {
                statusMsg.innerText = `正在处理第 ${i}/${pdf.numPages} 页...`;
                const page = await pdf.getPage(i);
                const textContent = await page.getTextContent();
                
                const lines = {};
                textContent.items.forEach(item => {
                    const y = Math.round(item.transform[5]);
                    if (!lines[y]) lines[y] = [];
                    lines[y].push(item);
                });

                const sortedY = Object.keys(lines).sort((a, b) => b - a);
                sortedY.forEach(y => {
                    const lineText = lines[y].sort((a, b) => a.transform[4] - b.transform[4])
                                            .map(item => item.str).join(' ');
                    
                    if (lineText.trim()) {
                        docChildren.push(new docxLib.Paragraph({
                            children: [new docxLib.TextRun(lineText)]
                        }));
                    }
                });

                if (i < pdf.numPages) {
                    docChildren.push(new docxLib.Paragraph({
                        children: [new docxLib.TextRun({ break: 1 })],
                        pageBreakBefore: true
                    }));
                }
            }

            statusMsg.innerText = '正在生成 Word 文档文件...';
            const doc = new docxLib.Document({
                sections: [{
                    children: docChildren
                }]
            });

            const blob = await docxLib.Packer.toBlob(doc);
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = currentFile.name.replace('.pdf', '.docx');
            link.click();

            statusMsg.className = 'status-msg success';
            statusMsg.innerText = '✅ 转换完成！已开始下载。';
        } catch (e) {
            console.error(e);
            statusMsg.className = 'status-msg error';
            statusMsg.innerText = '❌ 转换失败：' + e.message;
        } finally {
            convertBtn.disabled = false;
            convertBtn.innerText = '立即转换为 Word (DOCX)';
        }
    };

    clearBtn.onclick = () => {
        currentFile = null;
        dropZone.style.display = 'block';
        fileInfo.style.display = 'none';
        toolActions.style.display = 'none';
        statusMsg.innerText = '';
        fileInput.value = '';
    };
</script>
{{< /rawhtml >}}

{{< rawhtml >}}
<div class="related-tools" data-current="to-word">
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
                <span class="desc">本地生成可编辑文档</span>
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
                <span class="desc">优化并减小文件体积</span>
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
    .tool-link .icon { font-size: 1.25rem; }
    .tool-link .label { font-weight: 600; font-size: 0.95rem; }
    [data-current="preview"] #link-preview, [data-current="merge"] #link-merge, [data-current="to-image"] #link-to-image, [data-current="to-pdf"] #link-to-pdf, [data-current="compress"] #link-compress, [data-current="to-word"] #link-to-word { display: none; }
</style>
{{< /rawhtml >}}

### 为什么选择我们的工具？

- **隐私安全**：文件不上传服务器，在本地完成处理。
- **完全免费**：无水印，无次数限制。
- **极速处理**：直接在您的浏览器中运行。
