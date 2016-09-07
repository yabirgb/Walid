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
  links: [{link:String, status: {type: Boolean, default: false},date: { type: Date, default: Date.now }, private:{type: Boolean, default: false}}],
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

  if ("entities" in msg){
    for (var e = 0; e < msg.entities.length; e++) {
      if(msg.entities[e].type === 'url'){
        var parts = msg.text.split(" ");
        var url = checker(parts);

        User.findOneOrCreate({username: msg.from.username}, {username: msg.from.username, telegramId: msg.from.id, secret: crypto.randomBytes(32).toString('hex')}, function(err, person) {
          if(err){
            bot.sendMessage(chatId, err)
          }
          //Avoid repeting url and able to add multiple
          // for each url
          for (var i = 0; i < url.length; i++) {
            //if no links
            if (person.links.length === 0) {
              person.links.push({link: url[i]});
            }
            else{
              //Initialy we havent found it
              var found = false;
              //for each link in database
              for (var z = 0; z < person.links.length; z++) {
                //If we find it change the var
                if (url[i] === person.links[z].link && person.links.length !== 0 ) {
                  found = true;
                  break;
                }
              }
              //If we have not found it
              if (found === false)
              {
                //Save it
                person.links.push({link: url[i]});
              }
            }
            person.save(function (err) {
              if (err) return handleError(err);
            });
            //Tell the user if we add or is already in
            if(found === false){
              bot.sendMessage(chatId, 'Added ' + url.join(" ") + " to the database");
            }
            else{
              bot.sendMessage(chatId, "This url is already on my database, I'm not adding it for now.");
            }
          }//end "for" for url
        }) //end of find or create
      }// end of spin throw entities that are url
    }//end with entities
  }//check if there are any entities

  //if there is not any url
  else{
    bot.sendMessage(chatId, "Sadly I'm not programmed to understand you :(");
  }


});
