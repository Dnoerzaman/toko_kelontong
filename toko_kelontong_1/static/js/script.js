function tambahRow() {
    const div = document.createElement('div');
    div.className = 'barang-row';
    div.innerHTML = document.querySelector('.barang-row').innerHTML;
    document.getElementById('form-barang').appendChild(div);
}

function hapusRow(button) {
    const rows = document.querySelectorAll('.barang-row');
    if (rows.length > 1) {
        button.parentElement.remove();
    }
}