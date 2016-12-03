var treeListTemplate;
var binominaltemplate;
var treeDetailsTemplate;
var searchMap;

//This function join the json to reconstuct one tree data
function completeInfo(idTree){
    if (typeof arbre[idTree] === "undefined"){
        return undefined;
    }
    else {
        var currentTree = jQuery.extend(true, {}, arbre[idTree]);

        if (typeof currentTree.nomBinominal === 'string') {
            currentTree.nomBinominal = jQuery.extend(true, {}, nomBinominal[currentTree.nomBinominal]);
            currentTree.nomBinominal.feuillage = jQuery.extend(true, {}, feuillage[currentTree.nomBinominal.feuillage]);
        }
        return(currentTree);
    }
}

function searchID() {
    searchMap.clearMap();
    $('#binominalDropdown').dropdown('restore defaults');
    let idTree = document.getElementById("idTree").value.trim().toLowerCase();
    var tree = completeInfo(idTree);
    if (typeof tree === 'undefined'){
        updateTreeDetails(undefined);
        updateTreeList([]);
    }
    else {
        searchMap.setMarker(tree);
        updateTreeDetails(tree);
        updateTreeList([tree]);
    }

}

function updateTreeDetails(tree) {
    $("#treeDetails").empty();
    if (typeof tree !== 'undefined'){
        var rendered = Mustache.render(treeDetailsTemplate, tree);
        $("#treeDetails").append(rendered);
    }
}

function updateTreeList(trees) {
    $("#treeList").empty();
    var rendered = Mustache.render(treeListTemplate, {trees: trees});
    $("#treeList").append(rendered);
}


function searchBinominalName(binName){
    searchMap.clearMap();
    let temp = [];
    jQuery.each(arbre, function(i, val) {
        if(val.nomBinominal == binName) {
            let tree = completeInfo(val.id);
            temp.push(tree);
            searchMap.setMarker(tree);
        }});
    updateTreeList(temp);

    searchMap.resetView();

    $(".resultListItem").hover(
        function(){
            $(this).css("background-color", "#89C4F4");
            searchMap.highlightMarker(arbre[$(this).attr('id')]);
        },
        function(){
            $(this).css("background-color", "transparent");
            searchMap.unhighlightMarker(arbre[$(this).attr('id')]);
    });

    $( ".resultListItem" ).dblclick(function() {
        let tree = completeInfo($(this).attr('id'));
        searchMap.setViewToMarker(tree);
        updateTreeDetails(tree);
    });
}

$( document ).ready(function() {
    treeListTemplate = $('#treeListTemplate').html();
    binominaltemplate = $('#binominalNameTemplate').html();
    treeDetailsTemplate = $('#treeDetailsTemplate').html();

    searchMap = new SearchMap("mapId");

    $('#binominalDropdown')
    .dropdown({
        forceSelection: false,
        onChange: function(dropdownValue, text, $selectedItem) {
            searchBinominalName(dropdownValue);
        }
    });

    var rendered = Mustache.render(binominaltemplate, {name: Object.keys(nomBinominal)});
    $("#binominalName-menu").append(rendered);
});
