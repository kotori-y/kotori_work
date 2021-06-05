function isNumeric(str) {
  if (typeof str != "string") return false; // we only process strings!
  return (
    !isNaN(str) && // use type coercion to parse the _entirety_ of the string (`parseFloat` alone does not do this)...
    !isNaN(parseFloat(str)) &&
    parseFloat(str) > 0
  ); // ...and ensure strings of whitespace fail
}

function show() {
  document.querySelector("svg").innerHTML = "";
  const colors = document.getElementById("colorMap").value.trim().split(/\s+/);
  let scale = document.getElementById("scale").value.trim();

  if (!isNumeric(scale)) {
    console.log(scale);
    alert("invalid input of scaled ratio!");
    return;
  }

  scale = parseFloat(scale);
  var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height"),
    innerRadius = 180,
    outerRadius = Math.min(width, height) / 2,
    g = svg
      .append("g")
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

  var x = d3
    .scaleBand()
    .range([0, 2 * Math.PI])
    .align(0);

  var y = d3.scaleRadial().range([innerRadius, outerRadius]);
  console.log(y);

  //   var z = d3
  //     .scaleOrdinal()
  //     .range([
  //       "#98abc5",
  //       "#8a89a6",
  //       "#7b6888",
  //       "#6b486b",
  //       "#a05d56",
  //       "#d0743c",
  //       "#ff8c00",
  //     ]);

  var z = d3.scaleOrdinal().range(colors);

  d3.csv(
    "level2.csv",
    function (d, i, columns) {
      for (i = 2, t = 0; i < columns.length; ++i)
        t += d[columns[i]] = +d[columns[i]];
      d.total = t;
      return d;
    },
    function (err, data_) {
      const data = [];
      let temp = "";
      for (let i = 0; i < data_.length; i++) {
        const flag = data_[i].firstLevel;
        if (flag !== temp) {
          data.push({
            secondLevel: `U${i}`,
            firstLevel: 0,
            "[0, 50)": 0,
            "[50, 100)": 0,
            "[100, 200)": 0,
            "[200, 300)": 0,
            "[300, 400)": 0,
            "[400, 600)": 0,
            "[600, )": 0,
            firstLevel: "U",
          });
          temp = flag;
        }
        data.push(data_[i]);
      }
      data.columns = data_.columns;
      //   console.log(data);

      x.domain(
        data.map(function (d) {
          return d.secondLevel;
        })
      );
      y.domain([
        0,
        d3.max(data, function (d) {
          return d.total / scale;
        }),
      ]);
      z.domain(data.columns.slice(2));

      const hashed = new Map();
      for (let i = 0; i < data.length; i++) {
        let c = data[i].firstLevel;
        c = c === "U" ? "" : c;
        hashed.set(c, (hashed.get(c) | 0) + 1);
      }

      flag = "";
      let tem = 0;
      for (let j = 0; j < data.length - 2; j++) {
        let c = data[j].firstLevel;
        c = c === "U" ? "" : c;
        const n =
          hashed.get(c) % 2 === 1
            ? (hashed.get(c) + 1) / 2
            : Math.ceil(hashed.get(c) / 2);
        if (c && c !== flag) {
          // console.log(c);
          tem = 0;
          flag = c;
        }
        if (tem !== n - 1) {
          c = "";
        }
        data[j].flag = c;
        tem++;
      }

      var label = g
        .append("g")
        .selectAll("g")
        .data(data)
        .enter()
        .append("g")
        .attr("text-anchor", "middle")
        .attr("transform", function (d) {
          //   if (d.secondLevel.match(/U\d/)) {
          //     return;
          //   }
          return (
            "rotate(" +
            (((x(d.secondLevel) + x.bandwidth() / 2) * 180) / Math.PI - 90) +
            ")translate(" +
            innerRadius +
            ",0)"
          );
        });

      label.append("line").attr("x2", -5).attr("stroke", "#000");

      label
        .append("text")
        .attr("transform", function (d) {
          return x(d.secondLevel) + x.bandwidth() / 2 + Math.PI / 2 < 4.92
            ? "rotate(0)translate(-18, 4)"
            : "rotate(180)translate(18, 4)";
        })
        .text(function (d) {
          return d.secondLevel.match(/U\d/) ? "" : d.secondLevel;
        });

      label
        .append("text")
        .attr("transform", function (d) {
          return x(d.secondLevel) + x.bandwidth() / 2 + Math.PI / 2 < 4.92
            ? "rotate(0)translate(-50, 1)"
            : "rotate(180)translate(50, 1)";
        })
        .text(function (d) {
          return d.flag;
        })
        .attr("font-size", "14px")
        .attr("fill", "grey");

      var yAxis = g.append("g").attr("text-anchor", "middle");

      var yTick = yAxis
        .selectAll("g")
        .data(y.ticks(scale > 3 ? 2 : 5 / scale).slice(1))
        .enter()
        .append("g");

      yTick
        .append("circle")
        .attr("fill", "none")
        .attr("stroke", "grey")
        .attr("r", 145)
        .attr("stroke-width", "3")
        .attr("id", "wavy");

      g.append("g")
        .selectAll("g")
        .data(d3.stack().keys(data.columns.slice(2))(data))
        .enter()
        .append("g")
        .attr("fill", function (d) {
          // console.log(d.key);
          return z(d.key);
        })
        .selectAll("path")
        .data(function (d) {
          return d;
        })
        .enter()
        .append("path")
        .attr(
          "d",
          d3
            .arc()
            .innerRadius(function (d) {
              return y(d[0]);
            })
            .outerRadius(function (d) {
              return !d.data.secondLevel.match(/U\d/)
                ? y(d[1])
                : y(-15 / scale);
            })
            .startAngle(function (d) {
              return x(d.data.secondLevel);
            })
            .endAngle(function (d) {
              return x(d.data.secondLevel) + x.bandwidth();
            })
            .padAngle(0.01)
            .padRadius(innerRadius)
        )
        .attr("fill", function (d) {
          return !d.data.secondLevel.match(/U\d/) ? "" : "white";
        })
        .attr("stroke", function (d) {
          return d.data.secondLevel.match(/U\d/) ? "" : "black";
        })
        .attr("stroke-width", "0.5");

      //   yTick
      //     .selectAll("text")
      //     .data(dial)
      //     .enter()
      //     .append("text")
      //     .attr("x", 130)
      //     // tweak digit Y position a little to ensure it's centred at desired position
      //     .attr("y", "0.4em")
      //   .attr("font-size", "14px")
      //   .attr("fill", "grey")
      //     .attr("font-family", "italic")
      //     .text(function (d, i) {
      //       return d;
      //     })
      //     .attr("transform", function (d, i) {
      //       return "rotate(" + (-90 + (360 / dial.length) * i) + ")";
      //     });

      var legend = g
        .append("g")
        .selectAll("g")
        .data(data.columns.slice(2).reverse())
        .enter()
        .append("g")
        .attr("transform", function (d, i) {
          // console.log(i);
          return "translate(300," + (i * 20 + 100) + ")";
        });

      legend
        .append("rect")
        .attr("width", 18)
        .attr("height", 18)
        .attr("fill", z)
        .attr("stroke", "black");

      legend
        .append("text")
        .attr("x", 30)
        .attr("y", 9)
        .attr("dy", "0.35em")
        .text(function (d) {
          return d;
        });

      g.append("text")
        .attr("x", 290)
        .attr("y", 80)
        .attr("dy", "0.35em")
        .attr("font-size", "10px")
        .text("Degree");

      g.append("rect")
        .attr("x", 290)
        .attr("y", 95)
        .attr("width", 100)
        .attr("height", 150)
        .attr("stroke", "black")
        .attr("fill", "none")
        .attr("stroke-width", "0.5");
    }
  );
}
