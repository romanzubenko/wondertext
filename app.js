var express = require('express'),
	http = require('http'),
	path = require('path');

var app = express();

app.configure(function(){
	app.set('port', process.env.PORT || 3002);
	app.use(express.bodyParser());
	app.use(express.static(path.join(__dirname, 'public')));
});

app.get('/', function(req, res){
	res.sendfile('./routes/index.html');
});

app.post('/ajax/suggestions', function(req, res){
	var sentence = req.body.sentence;
	if( !sentence ) return;

	var nodeio = require('node.io'),
		options = { timeout: 10},
		myjob = new nodeio.Job(options, {
			input: ['"'+req.body.sentence.trim()+' " site:edu'],
			run: function (keyword) {
				console.log(keyword);
				this.getHtml('http://www.google.com/search?q=' + encodeURIComponent(keyword), function (err, $, src) {
					var contexts = [];
					if( src==undefined){
						console.log("Blocked by Google...");
					}else if( /No results found for /.test(src) ){
						contexts.push("No matches.");
					}else{
						try{
							$('span.st').each(function(href){
								var context = href.innerHTML;
								context = /[^\.]<\/b\>([\w\d\s\,]+)/g.exec(context);
								if( context!=null && context[1].trim()!="" )
									contexts.push(context[1].trim().toLowerCase());
							});
						}catch (e) {
							contexts.push("No matches.");
							//console.log(e);
						}
					}
					this.emit(contexts);
				});
			},
			fail: function(input, status) {
				console.log(input+' failed with status: '+status);
				this.emit('failed');
			}
		});

	nodeio.start(myjob, function (err, output) {
		console.log(output);
		res.send(JSON.stringify(output));
	}, true);
});

app.post('/ajax/suggestions2', function(req, res){

	//Python
	var sys = require('util');
	var exec = require('child_process').exec;
	function puts(error, stdout, stderr) {
		sys.puts(stdout);
		res.send(stdout);
	}
	exec("python ./suggestions/suggester.py '"+req.body.sentence+"'", puts);
});


//Google Connection Test
var	nodeio = require('node.io'),
	options = {timeout: 10},
	job = new nodeio.Job(options, {
	input: ['hello', 'foobar', 'weather'],
		run: function (keyword) {
			this.getHtml('http://www.google.com/search?q=' + encodeURIComponent(keyword), function (err, $) {
				var results = $('#resultStats').text.toLowerCase();
				this.emit(keyword + ' has ' + results);
			});
		}
	});

nodeio.start(job, function (err, output) {
	console.log(output);
}, true);


http.createServer(app).listen(app.get('port'), function(){
	console.log("Express server listening on port " + app.get('port'));
});