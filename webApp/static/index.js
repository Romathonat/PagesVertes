var treeListTemplate
var binominaltemplate

//This function join the json to reconstuct one tree data
function completeInfo(idTree){
    var currentTree = arbre[idTree];

    //here we are making the join, if necessary
    if (typeof currentTree["nomBinominal"] === 'string') {
        currentBinominalName = nomBinominal[currentTree["nomBinominal"]];
        currentBinominalName["feuillage"] = feuillage[currentBinominalName["feuillage"]];
        currentTree["nomBinominal"] = currentBinominalName;
    }
    return(currentTree)
}

function searchID() {
    clearMap()
    let idTree = document.getElementById("idTree").value.toLowerCase();
    var tree = completeInfo(idTree)
    setMarker(tree)
}

function searchBinominalName(binName){
    clearMap()
    let temp = []
    jQuery.each(arbre, function(i, val) {
        if(val.nomBinominal == binName) {
            let tree = completeInfo(val.id)
            temp.push(val)
            setMarker(tree)
        }})
    var rendered = Mustache.render(treeListTemplate, {trees: temp});
    $("#treeList").empty()
    $("#treeList").append(rendered);
}

$( document ).ready(function() {
    treeListTemplate = $('#treeListTemplate').html();
    binominaltemplate = $('#binominalNameTemplate').html();

    $('.ui.dropdown')
    .dropdown({
        onChange: function(dropdownValue, text, $selectedItem) {
            searchBinominalName(dropdownValue)
        }
    })

    var rendered = Mustache.render(binominaltemplate, {name: Object.keys(nomBinominal)});
    $("#binominalName-menu").append(rendered);
});
