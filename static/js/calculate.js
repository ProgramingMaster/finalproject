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

/*
  This function finds what weights to put on either side of the bar. After first subtracting the weight
of the bar from your weight, it starts at the beginning of the weights array and simulates adding
those weights to both sides of the bar by subtracting those weights from your weight.
  If the total weight is still greater than or equal to zero, then your can add those weights to the bar
(the result arr) without going over your weight. An important note is that you only add one of those
weights to the result arr. This is because the entire result arr will be shown twice (once on each side
of the bar). If your weight is now zero then your done and can return the result arr.
  Otherwise, if your weight is now less than zero, then try a smaller weight (by incrementing i).
If you've tried all the possible weights, then return the result arr like normal but with an extra line
that shows the remainding weight that needs to be added to each side.
  Another important note is that this function doesn't actually return just the result arr. It returns
result array as a string with a <br> tag between each element (which makes the string vertical).
*/
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