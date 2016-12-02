var treeListTemplate;
var binominaltemplate;
var treeDetailsTemplate;
var searchMap;

//This function join the json to reconstuct one tree data
function completeInfo(idTree){
    var currentTree = jQuery.extend(true, {}, arbre[idTree]);

    //here we are making the join, if necessary
    if (typeof currentTree.nomBinominal === 'string') {
        currentTree.nomBinominal = jQuery.extend(true, {}, nomBinominal[currentTree.nomBinominal]);
        currentTree.nomBinominal.feuillage = jQuery.extend(true, {}, feuillage[currentTree.nomBinominal.feuillage]);

    }
    return(currentTree);
}

function searchID() {
    searchMap.clearMap();
    let idTree = document.getElementById("idTree").value.toLowerCase();
    var tree = completeInfo(idTree);
    searchMap.setMarker(tree);
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
    var rendered = Mustache.render(treeListTemplate, {trees: temp});
    $("#treeList").empty();
    $("#treeList").append(rendered);

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
        let tree = completeInfo($(this).attr('id'))
        searchMap.setViewToMarker(tree);
        var rendered = Mustache.render(treeDetailsTemplate, tree);
        $("#treeDetails").empty();
        $("#treeDetails").append(rendered);
    });
}

$( document ).ready(function() {
    treeListTemplate = $('#treeListTemplate').html();
    binominaltemplate = $('#binominalNameTemplate').html();
    treeDetailsTemplate = $('#treeDetailsTemplate').html();

    searchMap = new SearchMap("mapId");

    $('.ui.dropdown')
    .dropdown({
        onChange: function(dropdownValue, text, $selectedItem) {
            searchBinominalName(dropdownValue);
        }
    });

    var rendered = Mustache.render(binominaltemplate, {name: Object.keys(nomBinominal)});
    $("#binominalName-menu").append(rendered);
});
