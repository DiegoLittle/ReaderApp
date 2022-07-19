/** @type {import('next').NextConfig} */
// module.exports = {
//   reactStrictMode: true,
//   images:{
//     domains:['lh3.googleusercontent.com']
//   },
//   future: {
//     webpack5: true
//   },
//   webpack: (config,options)=>{
//     config.experiments= {
//       "topLevelAwait": true,
//       "layers": true
//     }
//     return config
//   }
//   // webpack: (config) => {
//   //   // load worker files as a urls with `file-loader`
//   //   config.module.rules.unshift({
//   //     test: /pdf\.worker\.(min\.)?js/,
//   //     use: [
//   //       {
//   //         loader: "file-loader",
//   //         options: {
//   //           name: "[contenthash].[ext]",
//   //           publicPath: "_next/static/worker",
//   //           outputPath: "static/worker"
//   //         }
//   //       }
//   //     ]
//   //   });

//   //   return config;
//   // }
// }

// const withSourceMaps = require("@zeit/next-source-maps");
// const withImages = require("next-images");

module.exports = [
    [
        // withImages,
        {
            exclude: /\.svg$/
        }
    ],
    // withSourceMaps
],
{
    // env: { *** redacted *** },
    // publicRuntimeConfig: { *** redacted *** },
    webpack: (config, options) => {
      if (!options.isServer) {
        // config.resolve.alias["@sentry/node"] = "@sentry/browser";
        // config.resolve.fallback.fs = false;
        
      }
      config.module.rules.push({
        test: /\.svg$/,
        use: ["@svgr/webpack"]
      });
      config.experiments= {
        "topLevelAwait": true,
        "layers": true
      }
      return config;
    },
    reactStrictMode: true,
}