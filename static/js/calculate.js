function calWeights(id, weight) {
    // Checks to see if no weights are being shown right now. This is so that you don't calculate the
    // weights everytime you click the calculate button
    if (($('#weightsLeft' + id).is(':empty') || $('#weightsRight' + id).is(':empty'))) {

        // Find the weights to add to each side of the bar
        let weights = weightsToAdd(id, weight)

        // Display that on both sides of the bar
        $('#weightsLeft' + id).html(weights)
        $('#weightsRight' + id).html(weights)
    }
}

function calWarmup(id, weight, percent) {
    // Ensure percent was submitted
    if (percent === '') {
        return
    }

    // Ensure percent was (formatted as) a positive integer
    if (percent.search(/\D|(^0+$)/) != -1) {
        return
    }

    // Turn percent into a Number
    percent = Number(percent)

    // Ensure percent is less than 100
    if (percent >= 100) {
        return
    }

    // Get percent% of the total weight (this is the warmup)
    let warmupWeight = Number((weight * (percent * 0.01)).toFixed(2))

    // Display the warmup weight
    $('#warmupTotal' + id).text("Total: " + warmupWeight)

    // Calculate the weights to put on either side of the bar for the warmup
    let weights = weightsToAdd(id, warmupWeight)

    // Display what weights to put on either side of the bar
    $('#warmupLeft' + id).html(weights)
    $('#warmupRight' + id).html(weights)

    // Show warmup weights (previously invisible)
    $('#warmupWeights' + id).css("display", "inline")
}

function weightsToAdd(id, weight) {
    // Posible weights
    let weights = [45, 35, 25, 10, 5, 2.5]

    // What weights to put on either side of the bar
    let result = []

    // Subtract the weight of the bar from the total weight
    weight -= 45

    // If the weight is now less than or equal to zero then your weight is less than or equal to the weight of the bar so just return 0
    if (weight <= 0) {
        return 0
    }

    // What weight your trying to add
    let i = 0

    while (weight !== 0) {
        // So you've gone through all possible weights and your still not at zero then show the remainding weight
        // that you need to add to each side (along with the result array as normal)
        if (i >= weights.length) {
            let remainder = "R: " + Number((weight / 2).toFixed(1))
            return result.length > 0 ? result.join('<br>') + '<br>' + remainder : remainder
        }

        // Tries to add whatever weight i is on (arr[i]) to both sides of the bar (by subtracting that weight
        // from your weight).
        if (weight - weights[i] * 2 >= 0) {
            weight -= weights[i] * 2
            result.push(String(weights[i]))
        }
        // Moves on to the next weight if the current weight if too big
        else {
            i++
        }
    }
    // Returns the result array as a string with a <br> tag between each element (which makes the string vertical).
    return result.join('<br>')
}