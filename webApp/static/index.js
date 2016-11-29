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
    let idTree = document.getElementById("idTree").value.toLowerCase();
    var tree = completeInfo(idTree)
    setMarker(tree)
}

$( document ).ready(function() {
    $('.ui.dropdown')
    .dropdown({
        onChange: function(dropdownValue, text, $selectedItem) {
            clearMap()
            jQuery.each(arbre, function(i, val) {
                if(val.nomBinominal == dropdownValue) {
                    let tree = completeInfo(val.id)
                    setMarker(tree)
                }
        })}
    });

    let binominaltemplate = $('#binominalNameTemplate').html();
    var rendered = Mustache.render(binominaltemplate, {name: Object.keys(nomBinominal)});
    $("#binominalName-menu").append(rendered);
});
