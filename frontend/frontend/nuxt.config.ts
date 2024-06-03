// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    devtools: {enabled: true},
    modules: ["@nuxtjs/tailwindcss", "@sidebase/nuxt-auth"],
    auth: {
        provider: {
            type: 'local',
            endpoints: {
                signUp: {path: '/register', method: 'post'},
                signIn: {path: '/login', method: 'post'},
                signOut: {path: '/login', method: 'post'},
                getSession: {path: '/me', method: 'get'}
            },
            pages: {
                login: '/auth/login'
            },
            token: {
                signInResponseTokenPointer: "/tokens/accessToken"
            }
        },
        baseURL: "http://localhost:8000",
        globalAppMiddleware: true
    }
})