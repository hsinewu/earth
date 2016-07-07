if(!process.argv[2])
    console.log('plz supply file name')
var Canvas = require('canvas'),
    fs = require('fs');

let argv = process.argv.slice(2)
argv.forEach((f)=>dofile(f))

function dofile(file){
    let c = new Canvas(2048,1024)
    // let c = new Canvas(4096,2048)
    let ctx = c.getContext('2d')
     
    let out = fs.createWriteStream(__dirname + '/' + file.replace(/\.[^/.]+$/, '') + '.png')
      , stream = c.createPNGStream();
     
    stream.on('data', function(chunk){
      out.write(chunk);
    });

    console.log(`reading ${file}...`)
    // TODO: would it be helpful to async?
    let data = fs.readFileSync(file).toString()
    // let data = fs.readFile(file, (err, data) => {
    //     if (err) throw err;
        // TODO: can I make it in a stream way?
        // data = data.toString();
        let lines = data.split('\n');
        for(let i=0; i<lines.length;){
            let [level, size] = lines[i].split(' ').map(Number);
            i++;
            if (size == 0) continue
            let hue = mapTo(level, -40, 40, 240, 0)
            ctx.strokeStyle = `hsl(${hue},100%,50%)`
            ctx.beginPath();
            for (let j=0; j<size; j+=2) {
                let [x, y] = lines[i+j].split(' ').map(Number);
                let [x2, y2] = lines[i+j+1].split(' ').map(Number);
                y = mapTo(y, -90, 90, 0, c.height)
                y2 = mapTo(y2, -90, 90, 0, c.height)
                x = mapTo(x, 0, 360, 0, c.width)
                x2 = mapTo(x2, 0, 360, 0, c.width)
                ctx.moveTo(x, y);
                ctx.lineTo(x2, y2);
            }
            ctx.stroke();
            i += size;
        }

    //})
}

function mapTo(value, fromlower, fromupper, tolower, toupper){
    // if(value==fromlower) return tolower;
    return (value - fromlower)/(fromupper-fromlower) * (toupper - tolower) + tolower
}