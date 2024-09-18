document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-upload');
    const fileList = document.getElementById('file-list');
    const processingStatus = document.getElementById('processing-status');
    const downloadLink = document.getElementById('download-link');

    fileInput.addEventListener('change', updateFileList);
    form.addEventListener('submit', handleSubmit);

    function updateFileList() {
        fileList.innerHTML = '';
        for (const file of fileInput.files) {
            const li = document.createElement('li');
            li.textContent = file.name;
            fileList.appendChild(li);
        }
    }

    async function handleSubmit(e) {
        e.preventDefault();
        
        if (fileInput.files.length === 0) {
            alert('Please select at least one image file.');
            return;
        }

        const formData = new FormData();
        for (const file of fileInput.files) {
            formData.append('files[]', file);
        }

        processingStatus.classList.remove('hidden');
        downloadLink.classList.add('hidden');

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            if (response.ok) {
                processingStatus.classList.add('hidden');
                downloadLink.classList.remove('hidden');
                downloadLink.querySelector('a').href = `/download/${result.csv_path}`;
            } else {
                throw new Error(result.error || 'An error occurred during processing.');
            }
        } catch (error) {
            console.error('Error:', error);
            alert(error.message);
            processingStatus.classList.add('hidden');
        }
    }
});
