import { HttpInterceptorFn } from '@angular/common/http';

export const authInterceptor: HttpInterceptorFn = (req, next) => {
  let token = null;

  // Verifica se estamos rodando no navegador antes de chamar o localStorage
  if (typeof window !== 'undefined') {
    token = localStorage.getItem('access_token');
  }

  // Se o token existir, injeta ele no cabeçalho (Header) da requisição
  if (token) {
    const authReq = req.clone({
      setHeaders: {
        Authorization: `Bearer ${token}`,
      },
    });
    return next(authReq);
  }

  // Se não tiver token, segue sem ele
  return next(req);
};
