function updateElementIndex(el, prefix, ndx) {
        var id_regex = new RegExp('(' + prefix + '-\\d+)');
        var replacement = prefix + '-' + ndx;
        if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
        if (el.id) el.id = el.id.replace(id_regex, replacement);
        if (el.name) el.name = el.name.replace(id_regex, replacement);
    }

    function addForm(btn, prefix) {
        var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        var row = $('.dynamic-form:first').clone(true).get(0);
        
        $(row).find('.delete-row').click(function() {
            deleteForm(this, prefix);
        });
        $('#id_' + prefix + '-TOTAL_FORMS').val(formCount);
        return false;
    }

    function deleteForm(btn, prefix) {
        debugger;
        $(btn).parents('.dynamic-form').remove();
        var forms = $('.dynamic-form');
        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            $(forms.get(i)).children().not(':last').children().each(function() {
                updateElementIndex(this, prefix, i);
            });
        }
        return false;
    }

   /* $(document).ready(function(){
        debugger;
        var addBtn = document.querySelector(".add-row");
        if(addBtn){
            addBtn.click = function() {
            alert("Hello!");};
            $('.add-row').click(function() {
                debugger;
                return addForm(this, 'form');
            };
        }
        $('.delete-row').click(function() {
    	    return deleteForm(this, 'form');
        });
    });*/