import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
// 1. Adicionamos o withFetch aqui na importação:
import { provideHttpClient, withInterceptors, withFetch } from '@angular/common/http';
import { authInterceptor } from './core/auth.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    // 2. Adicionamos o withFetch() aqui dentro:
    provideHttpClient(withFetch(), withInterceptors([authInterceptor])),
  ],
};
