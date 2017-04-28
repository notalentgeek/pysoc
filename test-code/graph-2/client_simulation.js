var client_simulation_array = [];
var client_simulation_name_array = [
  "carl",
  "chris",
  "dennet",
  "richard",
  "neil",
  "sam"
];

function client_simulation (_name) {
  client_simulation_array.push(this);
  this.name = _name;

  this.client_circle = null;
  this.client_circle_color = INTRGB(HashCode(this.name));
  this.latest_amount_face = 0;
  this.latest_amount_pitch = 0;
  this.latest_amount_volume = 0;
  this.latest_presence_client_simulation_circle_array = [];
  this.latest_presence_client_simulation_name_array = [];
  this.online = false;
  this.online_chance = 1.0;
}
client_simulation.prototype.contructor = client_simulation;
client_simulation.prototype.simulate = function () {
  if (this.online) {
    this.simulate_detection();
  }
};
client_simulation.prototype.simulate_detection = function () {
  this.simulate_detection_face();
  this.simulate_detection_pitch();
  this.simulate_detection_presence();
  this.simulate_detection_volume();
};
client_simulation.prototype.simulate_detection_face = function () {
  this.latest_amount_face = 0;
  for (var i = 0; i < client_simulation_array.length; i ++) {
    if(
        (client_simulation_array[i].name != this.name) &&
        (client_simulation_array[i].online)
    ){
      this.latest_amount_face ++;
    }
  }
};
client_simulation.prototype.simulate_detection_pitch = function () {
  // Number.
  this.latest_amount_pitch = (Math.random()*2500.0).toFixed(3);
  // Animation.
  var fill_temp = ShadeRGBColor("rgb(" + HexRGB(this.client_circle_color).r + ", " + HexRGB(this.client_circle_color).g + ", " + HexRGB(this.client_circle_color).b +")", scale_linear_pitch(this.latest_amount_pitch));
  this.client_circle.circle.style("fill", fill_temp);
};
client_simulation.prototype.simulate_detection_presence = function () {
  this.latest_presence_client_simulation_circle_array = [];
  this.latest_presence_client_simulation_name_array = [];

  for (var i = 0; i < client_simulation_array.length; i ++) {
    if (
      (!client_simulation_array[i].client_circle) &&
      (client_simulation_array[i].name != this.name) &&
      (client_simulation_array[i].online)
    ) {
      this.latest_presence_client_simulation_circle_array.push(client_simulation_array[i].client_circle);
      this.latest_presence_client_simulation_name_array.push(client_simulation_array[i].name);
    }
  }
};
client_simulation.prototype.simulate_detection_volume = function () {
  // Number.
  this.latest_amount_volume = (Math.random()*0.1).toFixed(3);
  // Animation.
  this.client_circle.radius = scale_linear_volume(this.latest_amount_volume);
  this.client_circle.circle.attr("r", this.client_circle.radius);
};
client_simulation.prototype.simulate_online = function () {
  var random = Math.random();
  if (random < this.online_chance) {
    if (!this.online) {
      this.online = true;
      this.online_chance = 1.0;
    }
    else {
      this.online_chance -= 0.05;
    }
  }
  else {
    if (this.online) {
      this.online = false;
      this.online_chance = 0;
    }
    else {
      this.online_chance += 0.05;
    }
  }
};

for(var i = 0; i < client_simulation_name_array.length; i ++){
    var client_temp = new client_simulation(
        client_simulation_name_array[i],
        true
    );
    new client_circle_simulation(client_temp, 180);
}
determine_target_for_client_circle_simulation(client_circle_simulation_array.length);
for(var i = 0; i < client_circle_simulation_array.length; i ++){
    client_circle_simulation_array[i].rotate_auto();
}