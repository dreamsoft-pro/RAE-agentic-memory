javascript
function click() {
    $state.go('client-zone-my-photos', {folderid: [this.folderData._id]});
    fullwidth.parentNode.removeChild(fullwidth);
}

const createFolderInfoElement = () => {
    const elem = document.createElement('div');
    elem.className = 'folderDataInfo';

    const titleElem = document.createElement('h3');
    titleElem.innerHTML = this.folderData.folderName;

    const link = document.createElement('a');
    link.className = 'btn btn-success';
    link.innerHTML = 'Zobacz folder';
    link.addEventListener('click', click.bind(this));

    elem.appendChild(titleElem);
    elem.appendChild(link);

    return elem;
};

// [BACKEND_ADVICE] Consider moving the logic of creating UI elements to a service if it involves complex interactions with backend data.
