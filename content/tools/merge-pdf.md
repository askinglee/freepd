---
title: "PDF 合并 - 免费在线工具"
date: 2026-01-22
description: "快速将多份 PDF 文件合并为一个。纯本地浏览器处理，无需上传服务器，安全高效且完全免费。"
slug: merge-pdf
tags: ["PDF工具", "免费工具"]
categories: ["在线工具"]
---

## PDF 合并工具

{{< rawhtml >}}
<div id="pdf-merge-tool" class="pdf-tool-container">
    <div class="drop-zone" id="drop-zone">
        <p>拖拽 PDF 文件到这里，或 <span class="browse-btn">点击浏览</span></p>
        <input type="file" id="file-input" multiple accept=".pdf" style="display: none;">
    </div>

    <div id="file-list" class="file-list">
        <!-- 选中的文件将显示在这里 -->
    </div>

    <div class="actions main-actions">
        <button id="merge-btn" class="primary-btn btn-large" disabled>
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20m-8-8l8 8 8-8"/></svg>
            立即合并 PDF 文件
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
    margin: 0;
    padding: 0;
    border: none;
    border-radius: 0;
    background: transparent;
    box-shadow: none;
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
    margin: 2rem 0;
}
.file-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    margin-bottom: 0.75rem;
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    transition: transform 0.2s;
}
.file-item:hover { transform: translateX(5px); }
.dark .file-item {
    background: #374151;
    border-color: #4b5563;
}
.file-info {
    display: flex;
    align-items: center;
}
.file-name {
    font-size: 0.95rem;
    color: #1f2937;
    font-weight: 500;
}
.dark .file-name { color: #f3f4f6; }
.remove-btn {
    color: #ef4444;
    cursor: pointer;
    font-size: 0.875rem;
    font-weight: 600;
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
    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
    color: white;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    font-weight: 600;
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.39);
}
.primary-btn:hover:not(:disabled) {
    transform: scale(1.02);
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.45);
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

<script src="https://unpkg.com/pdf-lib@1.17.1/dist/pdf-lib.min.js"></script>
<script>
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const fileList = document.getElementById('file-list');
    const mergeBtn = document.getElementById('merge-btn');
    const clearBtn = document.getElementById('clear-btn');
    const statusMsg = document.getElementById('status-msg');

    let filesArray = [];

    // 点击上传
    dropZone.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', (e) => {
        handleFiles(e.target.files);
    });

    // 拖拽上传
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
            if (file.type === 'application/pdf') {
                filesArray.push(file);
            }
        }
        updateFileList();
    }

    function updateFileList() {
        if (!fileList) return;
        fileList.innerHTML = '';
        filesArray.forEach((file, index) => {
            const item = document.createElement('div');
            item.className = 'file-item';
            item.innerHTML = `
                <div class="file-info">
                    <span class="file-name">${index + 1}. ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)</span>
                </div>
                <span class="remove-btn" onclick="removeFile(${index})">删除</span>
            `;
            fileList.appendChild(item);
        });

        mergeBtn.disabled = filesArray.length < 2;
        clearBtn.style.display = filesArray.length > 0 ? 'inline-block' : 'none';
    }

    window.removeFile = (index) => {
        filesArray.splice(index, 1);
        updateFileList();
    };

    clearBtn.addEventListener('click', () => {
        filesArray = [];
        updateFileList();
        statusMsg.innerHTML = '';
    });

    mergeBtn.addEventListener('click', async () => {
        try {
            mergeBtn.disabled = true;
            mergeBtn.innerText = '正在处理...';
            statusMsg.className = 'status-msg';
            statusMsg.innerText = '正在合并 PDF 文件，请稍候...';

            const { PDFDocument } = PDFLib;
            const mergedPdf = await PDFDocument.create();

            for (const file of filesArray) {
                const arrayBuffer = await file.arrayBuffer();
                const pdf = await PDFDocument.load(arrayBuffer);
                const copiedPages = await mergedPdf.copyPages(pdf, pdf.getPageIndices());
                copiedPages.forEach((page) => mergedPdf.addPage(page));
            }

            const mergedPdfBytes = await mergedPdf.save();
            const blob = new Blob([mergedPdfBytes], { type: 'application/pdf' });
            const url = URL.createObjectURL(blob);
            
            const link = document.createElement('a');
            link.href = url;
            link.download = `merged_${new Date().getTime()}.pdf`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);

            statusMsg.className = 'status-msg success';
            statusMsg.innerText = '✅ 合并成功！文件已开始下载。';
        } catch (error) {
            console.error(error);
            statusMsg.className = 'status-msg error';
            statusMsg.innerText = '❌ 合并失败：' + error.message;
        } finally {
            mergeBtn.disabled = false;
            mergeBtn.innerText = '立即合并 PDF';
        }
    });
</script>
{{< /rawhtml >}}
