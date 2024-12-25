document.addEventListener('DOMContentLoaded', function() {
    const searchField = document.getElementById('searchfield');
    const resultsMenu = document.getElementById('resultsmenu');
    const noResults = document.getElementById('no-results');
    console.log(document.getElementById('no-results'));
    const loading = document.getElementById('loading');
    const resultTemplate = document.getElementById('result-template');

    searchField.addEventListener('input', function() {
        const query = searchField.value.trim();
        if (query.length === 0) {
            resultsMenu.style.display = 'none';
            return;
        }

        noResults.style.display = 'none';
        loading.style.display = 'block';
        resultsMenu.style.display = 'block';

        $.ajax({
            url: '/search/',
            method: 'POST',
            data: {
                query: query
            },
            success: function(data) {
                loading.style.display = 'none';
                if (data.results.length === 0) {
                    noResults.style.display = 'block';
                } else {
                    noResults.style.display = 'none';
                    resultsMenu.innerHTML = '';
                    data.results.forEach(result => {
                        const resultItem = resultTemplate.cloneNode(true);
                        resultItem.style.display = 'block';
                        resultItem.querySelector('a').href = result.url;
                        resultItem.querySelector('a').textContent = result.title;
                        resultsMenu.appendChild(resultItem);
                    });
                }
            },
            error: function(error) {
                console.error('Error:', error);
                loading.style.display = 'none';
                noResults.style.display = 'block';
            }
        });
    });
});
