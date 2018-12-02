let categories = (dataiku.getWebAppConfig().categories||[]).map(it => ({name: it.from, description: it.to}));
let currentPath;

function drawApp(allItems) {
    try {
        dataiku.checkWebAppParameters();
    } catch (e) {
        alert(e.message + ' Go to settings tab');
    }
    drawCategories(categories);
    $('#skip').click(next)
    next();
}

function drawCategories(categories) {
    $('#category-buttons').empty();
    $('#category-descriptions').empty();
    categories.forEach(cat => {
        const button = $(`<button class="cat-button">${cat.name}</button>`)
        $('#category-buttons').append(button);
        if (cat.description) {
            const desc = $(`<li><strong>${cat.name}: </strong>${cat.description}</li>`)
            $('#category-descriptions').append(desc);
        }
    });
    if (categories.some(c => c.description)) {
        $('.right').show();
    }
    $('#category-buttons button').each((idx, button) => {
        $(button).click(() => { classify(categories[idx].name)})
    });
}

function next() {
    webappBackend.get('next', {}, updateProgress);
}

function drawItem() {
    if (!currentPath || !currentPath.length) {
        $('#app').html('<div id="done">The End</div><p>All the images were labelled (or skipped, refresh to see the skipped ones)</p>')
    } else {
        webappBackend.get('get-image-base64', {path: currentPath}, function(resp) {
            let contentType = 'image/png';
            $('#item-to-classify').html(`<img src="data:${contentType};base64,${resp.data}" />`);
            $('#comment').val('')
        });
    }
}

function classify(cat) {
    const comment = $('#comment').val()
    webappBackend.get('classify', {path: currentPath, comment: $('#comment').val(), cat: cat}, updateProgress);
}

function updateProgress(resp) {
    currentPath = resp.nextPath;
    $('#total').text(resp.total);
    $('#labelled').text(resp.labelled);
    $('#skipped').text(resp.skipped);
    drawItem();
}

const webappBackend = (function() {
    function getUrl(path) {
        return dataiku.getWebAppBackendUrl(path);
    }
    function get(path, args, done, fail) {
        return $.getJSON(getUrl(path), args, done, fail);
    }
    function post(path, args, done, fail) {
        return $.post(getUrl(path), args, done, fail);
    }
    return {getUrl, get, post}
})();

drawApp();