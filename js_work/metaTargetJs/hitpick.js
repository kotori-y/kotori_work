/*
 * @Description: hitpickv2 in JS
 * @Author: Kotori Y
 * @Date: 2020-12-30 15:00:46
 * @LastEditors: Kotori Y
 * @LastEditTime: 2020-12-30 17:32:27
 * @FilePath: \libc:\Users\0720\Desktop\py_work\kotori_work\js_work\metaTargetJs\hitpick.js
 * @AuthorMail: kotori@cbdd.me
 */

const request = require("request");
const cheerio = require("cheerio");
const sleep = require("./sleep.js");
// const { sleep } = require("./sleep.js");

const getStatusID = (smiles, callback) => {
  var data = {
    list_smiles: `1   ${smiles}`,
    exp: "",
  };
  request.post(
    {
      url:
        "http://mips.helmholtz-muenchen.de/HitPickV2/TargetPredictionController",
      formData: data,
    },
    function (err, resp, body) {
      if (err) {
        console.log(err);
      } else {
        var $ = cheerio.load(body);
        var statusID = /var fileId = "(.*?)";/.exec($.html());
        statusID = statusID ? statusID[1] : null;
        callback(null, statusID);
      }
    }
  );
};

const retryUntil = (url, callback) => {
  request.get(
    {
      url: url,
    },
    function (err, resp, body) {
      if (err) {
        console.log(err);
      } else {
        sleep.timer(2500);
        console.log(">>> running...")
        var $ = cheerio.load(body);

        $.html().includes("false")
          ? retryUntil(url, callback)
          : callback(null, $);
      }
    }
  );
};

const getResultID = (smiles, callback) => {
  getStatusID(smiles, function (err, statusID) {
    console.log(statusID);
    if (err) {
      console.log(err);
    } else {
      var url = `http://mips.helmholtz-muenchen.de/HitPickV2/StatusController?processID=${statusID}`;
      retryUntil(url, function (err, $) {
        if (err) {
          console.log(err);
        } else {
          var fid = $.text();
          callback(null, fid);
        }
      });
    }
  });
};

const getHitPickRes = (smiles, callback) => {
  getResultID(smiles, function (err, fid) {
    if (err) {
      console.log(err);
    } else {
      var download_url = `http://mips.helmholtz-muenchen.de/HitPickV2/results/${fid}/Step1_Results_Prediction/Results/all_compounds_targets.json`;
      request.get(
        {
          url: download_url,
        },
        function (err, resp, body) {
          var $ = cheerio.load(body);
          try {
            var body = JSON.parse($.text());
          } catch (error) {
            var body = { data: [] };
            console.log(error);
          }

          var _cols = [
            "Query Compound",
            "Predicted/Known Target",
            "Protein Complex",
            "Most Similar Compound",
            "Precision",
            "Tc",
          ];

          var _body = [];
          for (var row of body.data) {
            _body.push({
              "Query Compound": row[0],
              "Predicted/Known Target": row[2],
              "Protein Complex": row[3],
              Precision: row[5],
              Tc: row[4],
              "Most Similar Compound": row[1],
            });
          }
          callback(null, _cols, _body);
        }
      );
    }
  });
};


const smiles = "C[C@@]12C[C@H](O)C3C(CCC4=CC(=O)CC[C@]34C)C2CC[C@]1(O)C(=O)CO"
getHitPickRes(smiles, function (err, _cols, _body) {
  if (!err) {
    console.log(_cols);
    console.log(_body);
  } else {
    console.log(err)
  }
});
