document.addEventListener("DOMContentLoaded", () => {
    const gridItems = document.querySelectorAll('.grid-item');
    const clickedItems = [];

    document.getElementById('imageUploadBtn').addEventListener('click', function() {
        document.getElementById('fileInput').click();
    });

    document.getElementById('fileInput').addEventListener('change', function() {
        var file = this.files[0];
        var reader = new FileReader();
    
        reader.onload = function(event) {
            var imageUrl = event.target.result;
            document.getElementById('grid').style.backgroundImage = `url(${imageUrl})`;
        };
    
        reader.readAsDataURL(file);
    });

    document.getElementById("grid-rows").addEventListener('change', function() {
        var selected_value = parseInt(this.value);
        var grid = document.getElementById("grid");
        var grid_columns = parseInt(document.getElementById("grid-columns").value);

        grid.innerHTML = '';

        for(var i=0; i< selected_value*grid_columns; i++) {
            var grid_item = document.createElement('div');
            grid_item.classList.add('grid-item');
            grid_item.setAttribute('data-id', i);
            grid.appendChild(grid_item);
            addClickListener(grid_item);
        }

        grid.style.gridTemplateColumns = "repeat(" + grid_columns + ", 1fr)";
        grid.style.gridTemplateRows = "repeat(" + selected_value + ", 1fr)";
    });

    document.getElementById("grid-columns").addEventListener('change', function() {
        var selected_value = parseInt(this.value);
        var grid = document.getElementById("grid");
        var grid_rows = parseInt(document.getElementById("grid-rows").value);

        grid.innerHTML = '';

        for(var i=0; i< selected_value*grid_rows; i++) {
            var grid_item = document.createElement('div');
            grid_item.classList.add('grid-item');
            grid_item.setAttribute('data-id', i);
            grid.appendChild(grid_item);
            addClickListener(grid_item);
        }

        grid.style.gridTemplateColumns = "repeat(" + selected_value + ", 1fr)";
        grid.style.gridTemplateRows = "repeat(" + grid_rows + ", 1fr)";
    });

    function addClickListener(item) {
        item.addEventListener('click', () => {
            const itemId = item.dataset.id;
            
            if (item.classList.contains('clicked')) {
                const index = clickedItems.indexOf(itemId);
                if (index !== -1) {
                    clickedItems.splice(index, 1);
                    item.classList.remove('clicked');
                }
            } else {
                item.classList.add('clicked');
                clickedItems.push(itemId);
            }

            console.log(clickedItems)
            document.getElementById('clickedItems').value = clickedItems;
        });
    }

    gridItems.forEach(item => {
        addClickListener(item);
    })
});