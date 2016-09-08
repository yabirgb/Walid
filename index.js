const crypto = require('crypto');

var TelegramBot = require('node-telegram-bot-api');
var mongoose = require('mongoose');
var findOneOrCreate = require('mongoose-find-one-or-create');
var Schema = mongoose.Schema;

var valid_url = require('./url_check')

//TelegramToken
var token = '240521639:AAEOAEoYsEFNwqQWT7csYlxu5jVr4ErtInM';

//========================================
//Mongo

//User schema
var UserSchema = new Schema ({
  username: {type:String, default: null},
  telegramId: String,
  links: [{link:String, status: {type: Boolean, default: false},date: { type: Date, default: Date.now }, private:{type: Boolean, default: true}}],
  secret: String,
  time : { type : Date }
});
UserSchema.plugin(findOneOrCreate);

var User = mongoose.model('User', UserSchema)

console.log("==========================\n Starting all! \n========================== ");

//Database
mongoose.Promise = global.Promise;
mongoose.connect('mongodb://localhost/test');
var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function() {
  console.log("Connected database")
});

//========================================
//Telegram
var bot = new TelegramBot(token, {polling: true});

//Look for urls in a list
var checker = function(list){
  var final = [];
  for (var i = 0; i < list.length; i++) {
    if(valid_url(list[i])){
      final.push(list[i]);
    }
  }
  return final;
}

var atLeastOneURL = function(obj){
  if (obj.type === 'url'){
    return true
  }
}

//Get the user in database
var getUser = function(msg){
  var user;
  try{
    user = User.findOne({'telegramId':msg.from.id});
  }
  catch(e){
    user = new User({username:msg.from.username,telegramId: msg.from.id, secret: crypto.randomBytes(32).toString('hex')});
    user.save(function(err) {
      if (err) throw err;
    })
  }
  return user;
}


// Matches /echo [whatever]
bot.onText(/\/echo (.+)/, function (msg, match) {
  var fromId = msg.from.id;
  var resp = match[1];
  bot.sendMessage(fromId, resp);
});

bot.onText(/\/me/, function (msg, match) {
  var fromId = msg.from.id;
  bot.sendMessage(fromId, "from me")
});

bot.onText(/\/love/, function (msg) {
  var chatId = msg.chat.id;
  var opts = {
      reply_to_message_id: msg.message_id,
      reply_markup: JSON.stringify({
        keyboard: [
          ['Yes, you are the bot of my life ❤'],
          ['No, sorry there is another one...']]
      })
    };
    bot.sendMessage(chatId, 'Do you love me?', opts);
});

// Any kind of message
bot.on('message', function (msg) {
  var chatId = msg.chat.id;
  console.log("===========")
  console.log(msg);
  if ("entities" in msg){
    //Filter using the criteria of at least one url in the entities
    if(msg.entities.filter(atLeastOneURL)){
      var parts = msg.text.split(" ");
      var url = checker(parts);

      User.findOneOrCreate({username: msg.from.username}, {username: msg.from.username, telegramId: msg.from.id, secret: crypto.randomBytes(32).toString('hex')}, function(err, person) {
        if(err){
          bot.sendMessage(chatId, err)
        }
        for (var i = 0; i < url.length; i++) {
          var found = false;
          var sec = i;
          for (var z = 0; z < person.links.length; z++) {
            //If we find it change the var
            if (url[i] === person.links[z].link && person.links.length !== 0 ) {
              found = true;
              break;
            }
          }

          if (found === false)
          {
            User.update(
              { "secret": person.secret },
              { "$addToSet": { "links": {"link":url[i]} }},
              function(err, result) {
                if (err){
                  return handleError(err);
                }
              }
            );
            person.save(function (err) {
              if(err) { return handleError(err)}else{
                bot.sendMessage(chatId, "Added "+ url[sec] + " to the database")
              };

            });
          }
          else{
            bot.sendMessage(chatId, "I already have this link!")
          }
        }
      }) //end of find or create
    }// end of spin throw entities that are url
  }//check if there are any entities

  //if there is not any url
  else{
    bot.sendMessage(chatId, "Sadly I'm not programmed to understand you :(");
  }


});
