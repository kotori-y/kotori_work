/*
 * @Description:
 * @Author: Kotori Y
 * @Date: 2020-12-28 13:35:26
 * @LastEditors: Kotori Y
 * @LastEditTime: 2020-12-29 17:27:39
 * @FilePath: \spiderc:\Users\0720\Desktop\py_work\kotori_work\js_work\metaTargetJs\sea.js
 * @AuthorMail: kotori@cbdd.me
 */
"use strict";

// const axios = require("axios")
const createCsvWriter = require("csv-writer").createObjectCsvWriter;
const request = require("request");
const cheerio = require("cheerio");
// const fs = require('fs');

// let opts = {
//   host: "127.0.0.1",
//   port: 1081,
// };

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

const getResultUrl = (smiles, callback) => {
  var data = {
    ref_type: "library",
    ref_library_id: "default",
    query_type: "custom",
    query_custom_targets_paste: smiles,
  };

  return request.post(
    {
      url: "http://sea.bkslab.org/search",
      form: data,
    },
    function (err, resp, body) {
      if (!err) {
        var $ = cheerio.load(body);
        var resUrl = $("a").attr("href");
        // console.log(resUrl)
        callback(null, resUrl);
      }
    }
  );
};

const checkStatus = (url, callback) => {
  request.get(
    { url: `http://sea.bkslab.org${url}` },
    function (err, resp, body) {
      if (!err) {
        var $ = cheerio.load(body);
        var status = $.html().includes("pending");
        console.log(status)
        console.log(">>> waiting");
        return callback([status, $]);
      }
    }
  );
};

const getSeaResult = (smiles, callback) => {
  getResultUrl(smiles, async function (err, url) {
    if (err) {
      console.log(err);
    } else {
    //   console.log(url);

      var status = true;
      while (status) {
        await sleep(5000);
        var [status, $] = await new Promise((resolve, reject) => {
          checkStatus(url, resolve);
        });
      }
      console.log("success");
      var cols = $(".table.table-bordered th");
      var cols = cols.slice(1);
      var body = $("tbody").children('tr');

      var _cols = [];
      var _body = [];

      for (var i = 0; i < cols.length; i++) {
        _cols.push(cols.eq(i).text());
      }
    //   console.log(_cols);

      for (var a = 1; a < body.length; a++) {
        var temp = {};
        var $tds = body.eq(a).find("td");
        for (var b = 0; b < _cols.length; b++) {
          temp[_cols[b]] = $tds.eq(b).text().replace(/\s/g, "");
        }
        _body.push(temp);
      }
      callback(null, _cols, _body);
    }
  });
};

const fileName = "test.csv";
getSeaResult("O=C(C=Cc1cnc(c2c1scc2c1ccc(cc1)Br)N)NCCCn1cncc1", function (err, _cols, _body) {
  console.log({"headers":_cols})
  if (err) {
    console.log(err);
  } else {
    var header = [];
    for (var _col of _cols) {
      header.push({ id: _col, title: _col });
    }
    const csvWriter = createCsvWriter({
      path: fileName,
      header: header,
      append: true,
    });

    csvWriter
      .writeRecords(_body)
      .then(() => console.log("The CSV file was written successfully"));
  }
});
