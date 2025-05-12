// Groovy 2.4
import groovy.json.JsonOutput
import groovy.json.JsonSlurper
import java.util.Properties
import java.io.InputStream
import java.io.ByteArrayInputStream
import java.util.UUID

// Function to process the incoming JSON
def processJson(parsedJson) {
    parsedJson.data.giftCards.nodes.each { node ->
        if (node.order == null) {
            node.order = generateDummyOrder() // Replace null order with a dummy order
        }
		
		// Check if retailLocation is null and create a dummy object if it is
        if (node.order?.retailLocation == null) {
            node.order.retailLocation = generateDummyRetailLocation() // Create a dummy retail location
        }
		
		 // Check if sourceIdentifier is null and create a dummy value if it is
        if (node.order?.sourceIdentifier == null) {
            node.order.sourceIdentifier = generateDummySourceIdentifier() // Create a dummy source identifier
        }
    }
    return parsedJson // Return the modified JSON
}

// Function to generate a dummy order object
def generateDummyOrder() {
    return [
        id: "dummy_order_id_${UUID.randomUUID().toString().replace('-', '')}", // Unique ID
        name: "Dummy Order",
        sourceIdentifier: "dummy_source_identifier",
        sourceName: "dummy_source_name",
        retailLocation: [
            metafield: [
                value: "dummy_value"
            ]
        ]
    ]
}

// Function to generate a dummy retail location object
def generateDummyRetailLocation() {
    return [
        metafield: [
            value: "dummy_value"
        ]
    ]
}

// Function to generate a dummy source identifier
def generateDummySourceIdentifier() {
    return "dummy_source_identifier${""}" // Unique dummy source identifier
}

// Iterate through each data context stream
for (int i = 0; i < dataContext.getDataCount(); i++) {
    InputStream is = dataContext.getStream(i)
    Properties props = dataContext.getProperties(i)

    // Parse the incoming JSON from the input stream
    def parsedJson = new JsonSlurper().parse(is)

    // Process the parsed JSON to replace null orders with dummy orders
    def outputJson = processJson(parsedJson)

    // Convert the modified JSON to a stream to return to the document flow
    dataContext.storeStream(new ByteArrayInputStream(JsonOutput.toJson(outputJson).getBytes("UTF-8")), props)
}
