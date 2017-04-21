// angles in degrees
function sph2cart(radius, theta, phi) {

    theta = theta * Math.PI / 180;
    phi = phi * Math.PI / 180;
    return {
        x: radius * Math.sin(phi) * Math.cos(theta),
        y: radius * Math.sin(phi) * Math.sin(theta),
        z: radius * Math.cos(phi)
    };
}

function cart2sph(x, y, z) {

    with (Math) {
        return {
            r: hypot( x, y, z),
            t: atan2( y, x)/ PI*180,
            p: acos( z/ hypot( x, y, z))/ PI*180
        };
    }
}

function datetime(y, m, d, h) {
    if( y<1e3) console.log('year < 1000 not handled')
    var yyyy = '' + y
    var [mm, dd, hh] = [m,d,h].map(function(x) {
        x = '0' + x
        return x.length > 2? x.slice(1) : x
    })
    return yyyy + mm + dd + hh
}

// or yyyymmddhh
function deltaHour(yyyymmdd, dh) {
    var [_, yyyy, mm, dd] = /(\d{4})(\d{2})(\d{2})/.exec(yyyymmdd)
    ,   d = new Date(`${yyyy} ${mm} ${dd}`)
    d.setHours( d.getHours() + dh)
    return datetime( d.getFullYear(), d.getMonth()+1, d.getDate(), d.getHours() )
}

// function forecast45(y, m, d) {
//     var date = new Date(`${y} ${m} ${d}`)
//     ,   a = []
//     for(var i=0; i<45; i++) {
//         var str = datetime( date.getFullYear(), date.getMonth()+1, date.getDate(), 0)
//         a.unshift(str)
//         date.setDate( date.getDate() - 1)
//     }
//     return a
// }

// assume 16/12/01~10
function forecast_dummy(d) {
    var str = '201612', a = []
    for(var i=1; i<=d; i++)
        a.push(str+'0'+i)
    if(d==10) {
        a.pop();
        a.push(str+'10')
    }
    return a
}

function parseRequest() {
    var query = location.search.substr(1)
    ,   params = query.split("&");
    return params
        .map( (v)=> v.split('=').map(decodeURIComponent) )
        .reduce( function(ac, [k,v]) { 
            ac[k] = v;
            return ac;
        }, {} );
}
// functions above are pure

var viz = {date: '', item: '', pos: 0, timer_id: 0, type: '', dates: [], get max(){ return (viz.type == 'dataset'? 180: viz.dates.length*4-1)}}
var schema, setting1, three, reqs
var ROOTDIR = 'data';

function updateViz(viz_new) {
    Object.assign( viz, viz_new);
    if(viz.pos != bar.value) bar.value = viz.pos;
    if(viz.max != bar.max) bar.max = viz.max;
    legends.className = viz.item;

    if(viz.type == 'dataset') {
        var ymdh = deltaHour(viz.date, viz.pos * schema.dh)
        three.map = three.testLoad(viz.date, viz.item, ymdh);
        label.textContent = `${viz.date}: ${ymdh}`

        var ymdh2 = deltaHour(viz.date, (viz.pos+1) * schema.dh)
        three.testLoad(viz.date, viz.item, ymdh2)   // preload
    } else {
        var date = viz.dates[~~(viz.pos/(24/schema.dh))] + '00'  // WARN: check forecast function
        ,   ymdh = deltaHour(viz.date, viz.pos%(24/schema.dh) * schema.dh);   // WARN: assume dh to be a factor of 24
        three.map = three.testLoad(date, viz.item, ymdh);
        label.textContent = `${date}:  ${ymdh}`
    }
}

function switchPlay(on) {

    if(on && viz.pos < viz.max) {
        var timer_id = setTimeout( ()=>{switchPlay(true)}, setting1.playSpeed)
        ,   pos = viz.pos + 1;
        updateViz({pos, timer_id});
        playCtrl.children[0].setAttribute('viewBox', '0 0 36 36');
    } else {
        playCtrl.children[0].setAttribute('viewBox', '36 0 36 36');
        clearInterval(viz.timer_id);
    }

}

var setGeoCam = (lat, lng) => setSphereCam( lng+90, 90-lat)

function setSphereCam( theta, phi) {

    var start = cart2sph(three.camera.position.z, three.camera.position.x, three.camera.position.y);
    var tween = new TWEEN.Tween(start).to({
        r: 8, t: theta, p: phi
    }, 500)
    .onUpdate( function() {
        var point = sph2cart( start.r, start.t, start.p)
        three.camera.position.set( point.y, point.z, point.x);
        three.camera.lookAt( new THREE.Vector3(0,0,0));
    }).start();
    
}

function initThree() {
    three = {}
    var container = document.getElementById('container')
    ,   loader = new THREE.TextureLoader()
    ,   textures={};
    
    // init
    var scene = new THREE.Scene()
    ,   camera = new THREE.PerspectiveCamera( 75, window.innerWidth/window.innerHeight, 0.1, 1000 )
    ,   renderer = new THREE.WebGLRenderer();

    container.appendChild(renderer.domElement);
    renderer.setSize( window.innerWidth, window.innerHeight );
    camera.position.z = 12;

    var orbits = new THREE.OrbitControls( camera, renderer.domElement );
    orbits.maxDistance = 12;
    orbits.minDistance = 6;
    orbits.enablePan = false;
    orbits.autoRotate = true;   
    orbits.autoRotateSpeed = 1;

    var directLight = new THREE.DirectionalLight( 0xcccccc, 1)
    ,   ambientLight = new THREE.AmbientLight( 0xcccccc, .3);
    directLight.position.set(5,3,5);
    scene.add( directLight );
    scene.add( ambientLight );

    // earth
    var geometry = new THREE.SphereGeometry(5, 128, 128)
    ,   material = new THREE.MeshPhongMaterial();
    material.map = loader.load('textures/earthmap1k.jpg');
    material.bumpMap = loader.load('textures/earthbump1k.jpg');
    material.bumpScale = 0.1;
    material.specularMap = loader.load('textures/earthspec1k.jpg');
    material.map = loader.load('textures/earthmap4k.jpg');
    material.bumpMap = loader.load('textures/earthbump4k.jpg');
    var earthMesh = new THREE.Mesh(geometry, material);
    scene.add(earthMesh);

    // shell
    var geometryShell = new THREE.SphereGeometry(5.001, 128, 128)
    ,   materialShell = new THREE.MeshBasicMaterial();
    materialShell.map = loader.load(`${ROOTDIR}/${viz.date}/${viz.item}/${viz.date}.png`);
    materialShell.map.magFilter = THREE.NearestFilter
    materialShell.transparent = true;
    materialShell.opacity = setting1.opacity;
    var shellMesh = new THREE.Mesh(geometryShell, materialShell);
    scene.add(shellMesh);

    // galaxy
    var geometryGalaxy = new THREE.SphereGeometry(900, 128, 128)
    ,   materialGalaxy = new THREE.MeshBasicMaterial();
    materialGalaxy.map = loader.load('textures/galaxy.png');
    materialGalaxy.side = THREE.BackSide;
    var galaxyMesh = new THREE.Mesh(geometryGalaxy, materialGalaxy);
    scene.add(galaxyMesh);

    three.camera = camera;
    three.update = function(){
        orbits.update();
        TWEEN.update();
        renderer.render(scene, camera);
    }
    three.onResize = function() {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();

        renderer.setSize( window.innerWidth, window.innerHeight );
    }
    three.setShadow = function(on) {
        directLight.intensity  = +on;
        ambientLight.intensity =+!on +.3;
    }
    three.testLoad = function(date, item, ymdh) {
        var hash = date + item + ymdh;
        if(!textures[hash]) {
            textures[hash] = loader.load(`${ROOTDIR}/${date}/${item}/${ymdh}.png`)
            textures[hash].magFilter = THREE.NearestFilter
        }
        return textures[hash];
    }
    three.__defineSetter__('map', v => materialShell.map=v )
    three.__defineGetter__('map', ()=> materialShell.map )
    three.__defineSetter__('opacity', v => materialShell.opacity=v )
    three.__defineGetter__('opacity', ()=> materialShell.opacity )
    three.__defineSetter__('autoRotateSpeed', v => orbits.autoRotateSpeed=v )
    three.__defineGetter__('autoRotateSpeed', ()=> orbits.autoRotateSpeed )
}

window.onload = async () => {
    reqs = parseRequest()
    bar.value = 0;

    var on = 0;
    playCtrl.onclick = ()=>{switchPlay(on=!on)}

    if(reqs.hash)
        ROOTDIR = 'hash/' + reqs.hash;
    
    var resp = await fetch(`${ROOTDIR}/dataset.json`)
    var json = await resp.json();
    schema = json;
    
    initGui();
    initThree();
    window.addEventListener( 'resize', ()=>three.onResize(), false );
    
    var animate = ()=>{
        requestAnimationFrame( animate );
        three.update();
    }
    animate();
}

function initGui() {
    var gui0 = new dat.GUI();

    setting1 = {
        playSpeed: 450,
        rotationSpeed: 1,
        opacity: .6,
        shadow: true
    };

    var gui1 = gui0.addFolder('Effect')

    gui1.add(setting1, 'playSpeed', {
        slow: 1500, average: 450, fast: 140
    });
    gui1.add(setting1, 'rotationSpeed', -25, 25)
        .step(1)
        .onChange( v =>three.autoRotateSpeed=v );

    gui1.add(setting1, 'opacity', .0, 1.)
        .onChange( v =>three.opacity=v );
    gui1.add(setting1, 'shadow')
        .onChange( v =>three.setShadow(v) );

    var names = schema.names
    ,   date = names.indexOf( reqs.report) > -1? reqs.report: names[0]
    ,   dates = forecast_dummy( +date.slice(-4, -2) )
    ,   items = schema.items
    ,   item = items.indexOf( reqs.variable) > -1? reqs.variable: items[0]
    ,   view = reqs.view || 'dataset'
    ,   setting2 = { date, item, view };

    var gui2 = gui0.addFolder('Target');

    gui2.add(setting2, 'view', ['dataset', 'forecast'])
        .onChange( type => {
            updateViz({ type, pos: 0 })
        });
    
    gui2.add(setting2, 'date', names)
        .onChange( date => {
            var dates = forecast_dummy( +date.slice(-4, -2) );
            updateViz({date, dates});
        });

    gui2.add(setting2, 'item', items)   // TODO: reuse viz
        .onChange( item =>updateViz({item}) );

    Object.assign( viz, { date, dates, item, type:view })  // Three isn't ready, don't updateViz
    legends.className = item

    gui2.open();

}