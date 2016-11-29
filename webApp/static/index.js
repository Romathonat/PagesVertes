//This function join the json to reconstuct one tree data
function completeInfo(idTree){
    var currentTree = arbre[idTree];

    //here we are making the join, if necessary
    if (typeof currentTree["nomBinomial"] === 'string') {
        currentBinomialName = nomBinomial[currentTree["nomBinomial"]];
        currentBinomialName["feuillage"] = feuillage[currentBinomialName["feuillage"]];
        currentTree["nomBinomial"] = currentBinomialName;
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
                if(val.nomBinomial == dropdownValue) {
                    let tree = completeInfo(val.id)
                    setMarker(tree)
                }
        })}
    });

    let binomialtemplate = $('#binomialNameTemplate').html();
    var rendered = Mustache.render(binomialtemplate, {name: Object.keys(nomBinomial)});
    $("#binomialName-menu").append(rendered);
});
