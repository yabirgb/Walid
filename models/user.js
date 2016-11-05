var mongoose = require('mongoose');
var findOneOrCreate = require('mongoose-find-one-or-create');
var Schema = mongoose.Schema;

var UserSchema = new Schema ({
  username: {type:String, default: null},
  telegramId: String,
  links: [{link:String, status: {type: Boolean, default: false},date: { type: Date, default: Date.now }, private:{type: Boolean, default: true}}],
  secret: String,
  time : { type : Date },
  waitingReply: {type: Boolean, default: false},
  waitingTimezone: {type: Boolean, default: false},
  timezone: String,
});

UserSchema.plugin(findOneOrCreate);

module.exports = mongoose.model('User', UserSchema)
