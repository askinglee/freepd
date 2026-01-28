---
title: "图片转 PDF - 免费在线工具"
date: 2026-01-26
description: "免费在线图片转PDF工具，将多张JPG/PNG图片一键合成为标准PDF文档。本地处理，保护隐私，简单易用。"
slug: image-to-pdf
tags: ["PDF工具", "图片转PDF"]
keywords:
  - 图片转PDF
  - JPG转PDF
  - PNG转PDF
  - 图片合成PDF
  - 多图转PDF
  - 图片转PDF在线
  - 图片转PDF免费
  - 照片转PDF
categories: ["在线工具"]
---

## 图片转 PDF

{{< rawhtml >}}
<div id="image-to-pdf-tool" class="pdf-tool-container">
    <div class="drop-zone" id="drop-zone">
        <p>拖拽图片到这里 (JPG/PNG)，或 <span class="browse-btn">点击浏览</span></p>
        <input type="file" id="file-input" multiple accept="image/*" style="display: none;">
    </div>

    <div id="file-list" class="file-list">
        <!-- 选中的图片将显示在这里 -->
    </div>

    <div class="actions main-actions">
        <button id="convert-btn" class="primary-btn btn-large" disabled>
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20m-8-8l8 8 8-8"/></svg>
            立即生成 PDF 文档
        </button>
        <button id="clear-btn" class="secondary-btn btn-large" style="display: none;">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18m-2 0v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
            清空列表
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
.drop-zone:hover, .drop-zone.drag-over {
    border-color: #3b82f6;
    background: #eff6ff;
}
.browse-btn {
    color: #3b82f6;
    text-decoration: underline;
}
.file-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 1rem;
    margin: 2rem 0;
}
.file-item {
    position: relative;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    overflow: hidden;
    aspect-ratio: 1;
    background: #f3f4f6;
    transition: transform 0.2s;
}
.file-item:hover { transform: scale(1.05); }
.file-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}
.remove-btn {
    position: absolute;
    top: 5px;
    right: 5px;
    background: rgba(239, 68, 68, 0.9);
    color: white;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    text-align: center;
    line-height: 22px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
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
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 600;
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.39);
}
.primary-btn:hover:not(:disabled) {
    transform: scale(1.02);
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.45);
}
.primary-btn:disabled {
    background: #d1d5db;
    box-shadow: none;
    cursor: not-allowed;
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

.status-msg { margin-top: 1.5rem; font-size: 1rem; text-align: center; }
.success { color: #059669; font-weight: 500; }
.error { color: #dc2626; font-weight: 500; }
</style>

<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
<script>
    const { jsPDF } = window.jspdf;
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileList = document.getElementById('file-list');
    const convertBtn = document.getElementById('convert-btn');
    const clearBtn = document.getElementById('clear-btn');
    const statusMsg = document.getElementById('status-msg');

    let imagesArray = [];

    dropZone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('drag-over');
        handleFiles(e.dataTransfer.files);
    });

    function handleFiles(files) {
        for (let file of files) {
            if (file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    imagesArray.push({
                        name: file.name,
                        data: e.target.result,
                        type: file.type
                    });
                    updateFileList();
                };
                reader.readAsDataURL(file);
            }
        }
    }

    function updateFileList() {
        if (!fileList) return;
        fileList.innerHTML = '';
        imagesArray.forEach((img, index) => {
            const item = document.createElement('div');
            item.className = 'file-item';
            item.innerHTML = `
                <img src="${img.data}">
                <span class="remove-btn" onclick="removeImg(${index})">×</span>
            `;
            fileList.appendChild(item);
        });

        convertBtn.disabled = imagesArray.length === 0;
        clearBtn.style.display = imagesArray.length > 0 ? 'inline-block' : 'none';
    }

    window.removeImg = (index) => {
        imagesArray.splice(index, 1);
        updateFileList();
    };

    clearBtn.addEventListener('click', () => {
        imagesArray = [];
        updateFileList();
        statusMsg.innerHTML = '';
    });

    convertBtn.addEventListener('click', async () => {
        try {
            convertBtn.disabled = true;
            convertBtn.innerText = '正在生成...';
            statusMsg.className = 'status-msg';
            statusMsg.innerText = '正在将图片合成为 PDF，请稍候...';

            const doc = new jsPDF();
            
            for (let i = 0; i < imagesArray.length; i++) {
                if (i > 0) doc.addPage();
                
                const img = imagesArray[i];
                const pageWidth = doc.internal.pageSize.getWidth();
                const pageHeight = doc.internal.pageSize.getHeight();
                
                // 获取图片原始尺寸以保持比例
                const imgProps = doc.getImageProperties(img.data);
                const ratio = imgProps.width / imgProps.height;
                
                let width = pageWidth - 20;
                let height = width / ratio;
                
                if (height > pageHeight - 20) {
                    height = pageHeight - 20;
                    width = height * ratio;
                }
                
                const x = (pageWidth - width) / 2;
                const y = (pageHeight - height) / 2;
                
                doc.addImage(img.data, img.type.split('/')[1].toUpperCase(), x, y, width, height);
            }

            doc.save(`images_${new Date().getTime()}.pdf`);

            statusMsg.className = 'status-msg success';
            statusMsg.innerText = '✅ 转换成功！PDF 已开始下载。';
        } catch (error) {
            console.error(error);
            statusMsg.className = 'status-msg error';
            statusMsg.innerText = '❌ 转换失败：' + error.message;
        } finally {
            convertBtn.disabled = false;
            convertBtn.innerText = '立即生成 PDF';
        }
    });
</script>
{{< /rawhtml >}}

{{< rawhtml >}}
<div class="related-tools" data-current="to-pdf">
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
