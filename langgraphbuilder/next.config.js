/** @type {import('next').NextConfig} */
module.exports = {
  webpack(config) {
    return config
  },
  poweredByHeader: false,
  generateEtags: false,
  reactStrictMode: true,
  swcMinify: true,
}
