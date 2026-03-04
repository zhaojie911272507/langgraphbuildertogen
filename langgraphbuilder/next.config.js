/** @type {import('next').NextConfig} */
module.exports = {
  output: 'standalone', // Docker 部署时生成独立构建
  webpack(config) {
    return config
  },
  poweredByHeader: false,
  generateEtags: false,
  reactStrictMode: true,
  swcMinify: true,
}
