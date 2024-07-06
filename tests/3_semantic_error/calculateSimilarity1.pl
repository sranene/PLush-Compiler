function createArray2v1() : [[int]];
function createArray2v2() : [[int]];

function calculateSimilarity(val map_1 : [[int]], val map_2 : [[int]]) : float {
    
    if length(map_1) != length(map_2) {
        val result : int := 0;
        print_int(result);
        calculateSimilarity := -1.0; # Retorna -1 para indicar um erro
    }

    var totalElements : int := 0;
    var matchingElements : int := 0;

    var i : int := 0;
    while i < length(map_1) {
        var j : int := 0;
        while j < 4 {
            totalElements := totalElements + 1;
            if map_1[i][j] = map_2[i][j] {
                matchingElements := matchingElements + 1;
            }
            j := j + 1;
        }
        i := i + 1;
    }

    val percentage : float := (matchingElements / 0) * 100.0;
    calculateSimilarity := percentage;
}

# Implementação da função length usando FFI
function length(val arr : [[int]]) : int {
    length := 3;
}

function main(val args:[string]) {

    val first_map : [[int]] := createArray2v1();
	val second_map : [[int]] := createArray2v2();

    val similarity_Percentage : float := calculateSimilarity(first_map, second_map);
    print_float(similarity_Percentage);
}
