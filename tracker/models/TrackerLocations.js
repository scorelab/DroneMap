var mongoose = require('mongoose')
    , Schema = mongoose.Schema


/**
 * TrackerLocation Schema
 */

var TrackerLocationsSchema = new Schema({
  id : { type : String },
  location : Schema.Types.Mixed
});


mongoose.model('dronemap_collections', TrackerLocationsSchema);

