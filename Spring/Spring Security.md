---
tags: [spring, security, authentication, authorization]
sources: [Kata Spring Framework & HTTP.pdf]
---

# Spring Security

## 1. Проблема — зачем это существует?

Каждое web-приложение нуждается в защите: проверить что пользователь — это тот, кем называется (аутентификация), и что у него есть права на запрошенный ресурс (авторизация). Без фреймворка это десятки ручных проверок, уязвимости, несогласованность. Spring Security решает это через декларативную настройку — один раз описать правила, дальше фреймворк применяет их к каждому запросу.

## 2. Аналогия

Spring Security — как контроль доступа в бизнес-центре:
- **Фильтры** — охранники на каждом этапе входа (рамка металлодетектора, проверка пропуска, фейсконтроль)
- **AuthenticationManager** — начальник охраны, который решает: пустить или нет
- **UserDetailsService** — база данных пропусков (чья карточка, какие права)
- **SecurityContextHolder** — именной бейдж, который ты несёшь всё время, пока находишься в здании

## 3. Как работает

### Три уровня безопасности

```
Identification  — Кто ты? (ввод логина)
Authentication  — Докажи! (проверка пароля) 
Authorization   — Что тебе можно? (проверка прав/ролей)
```

### Filter Chain (цепочка фильтров)

Spring Security работает как цепочка `javax.servlet.Filter`, которая стоит **перед** `DispatcherServlet`:

```
HTTP Request
    ↓
DelegatingFilterProxy          ← Bridge между Servlet и Spring context
    ↓
FilterChainProxy               ← Управляет SecurityFilterChain
    ↓
SecurityFilterChain (цепочка):
  - SecurityContextPersistenceFilter  ← Загрузить SecurityContext из сессии
  - UsernamePasswordAuthenticationFilter ← Обработать POST /login
  - ExceptionTranslationFilter        ← 401/403 при ошибках
  - FilterSecurityInterceptor         ← Проверить права на ресурс
    ↓
DispatcherServlet
```

### Поток аутентификации (Authentication Flow)

```
1. POST /login (username + password)
        ↓
2. UsernamePasswordAuthenticationFilter
   → создаёт UsernamePasswordAuthenticationToken(username, password)
        ↓
3. AuthenticationManager (интерфейс)
   → реализация: ProviderManager
        ↓
4. ProviderManager перебирает AuthenticationProvider[]
   → DaoAuthenticationProvider (стандартный)
        ↓
5. DaoAuthenticationProvider:
   a. userDetailsService.loadUserByUsername(username) → UserDetails
   b. passwordEncoder.matches(rawPassword, encodedPassword)
        ↓
6. Если OK → UsernamePasswordAuthenticationToken(principal, null, authorities)
   (authenticated=true)
        ↓
7. SecurityContextHolder.getContext().setAuthentication(token)
        ↓
8. Сессия сохраняет SecurityContext
```

```java
// Реализация UserDetailsService — главная точка кастомизации:
@Service
@RequiredArgsConstructor
public class CustomUserDetailsService implements UserDetailsService {

    private final UserRepository userRepository;

    @Override
    public UserDetails loadUserByUsername(String username)
            throws UsernameNotFoundException {
        User user = userRepository.findByUsername(username)
            .orElseThrow(() -> new UsernameNotFoundException(username));

        return org.springframework.security.core.userdetails.User
            .withUsername(user.getUsername())
            .password(user.getPasswordHash())  // уже зашифрован в БД
            .roles(user.getRoles().toArray(String[]::new))
            .build();
    }
}
```

### Authentication объект

```java
Authentication auth = SecurityContextHolder.getContext().getAuthentication();

auth.getPrincipal();      // UserDetails или имя (кто)
auth.getCredentials();    // пароль (обычно null после аутентификации)
auth.getAuthorities();    // Collection<GrantedAuthority> — роли/права
auth.isAuthenticated();   // true если аутентифицирован
```

### Конфигурация SecurityFilterChain (Spring Boot 3+ / Spring Security 6)

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .requestMatchers("/api/**").authenticated()
                .anyRequest().denyAll()
            )
            .formLogin(form -> form
                .loginPage("/login")
                .defaultSuccessUrl("/dashboard")
            )
            .logout(logout -> logout
                .logoutUrl("/logout")
                .invalidateHttpSession(true)
            )
            .sessionManagement(session -> session
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS) // для JWT
            )
            .csrf(csrf -> csrf.disable()) // для REST API
            .build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
```

### @PreAuthorize / @Secured — метод-уровневая авторизация

```java
@EnableMethodSecurity  // включить в конфиге
@RestController
public class AdminController {

    @GetMapping("/admin/users")
    @PreAuthorize("hasRole('ADMIN')")
    public List<UserDto> getAllUsers() { ... }

    @DeleteMapping("/users/{id}")
    @PreAuthorize("hasRole('ADMIN') or #id == authentication.principal.id")
    public void deleteUser(@PathVariable Long id) { ... }

    @Secured("ROLE_ADMIN")  // аналог, но без SpEL
    public void adminOnly() { ... }
}
```

### JWT-аутентификация (без сессий)

```java
// Фильтр для JWT:
@Component
public class JwtAuthFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain)
            throws ServletException, IOException {

        String token = extractToken(request); // из заголовка Authorization
        if (token != null && jwtService.isTokenValid(token)) {
            UserDetails userDetails = userDetailsService
                .loadUserByUsername(jwtService.extractUsername(token));

            UsernamePasswordAuthenticationToken authToken =
                new UsernamePasswordAuthenticationToken(
                    userDetails, null, userDetails.getAuthorities());

            SecurityContextHolder.getContext().setAuthentication(authToken);
        }
        filterChain.doFilter(request, response);
    }
}
```

---

## 4. Глубже — что важно знать

**CSRF-защита:** Spring Security по умолчанию включает CSRF. Для REST API (stateless) обычно отключают — клиент использует JWT/токен вместо куки.

**PasswordEncoder:** никогда не хранить пароли в открытом виде. `BCryptPasswordEncoder` — стандарт: добавляет соль, медленный по дизайну, устойчив к brute-force.

**403 vs 401:** 
- `401 Unauthorized` — не аутентифицирован (нет токена/сессии)
- `403 Forbidden` — аутентифицирован, но нет прав

**SecurityContextHolder** по умолчанию использует `ThreadLocal` → контекст безопасности привязан к потоку. При async-обработке нужен `DelegatingSecurityContextExecutor`.

---

## 5. Связи с другими концепциями

- [[Spring Core IoC DI]] — SecurityFilterChain, UserDetailsService — Spring бины
- [[Spring Boot]] — `spring-boot-starter-security` автоматически добавляет базовую защиту
- [[Хранение паролей хеширование шифрование]] — BCrypt, соль, почему нельзя хранить в открытом виде
- [[Spring MVC REST (Controller vs RestController)]] — Security фильтры стоят перед DispatcherServlet

## 6. Ответ на собесе (2 минуты)

> "Spring Security — это цепочка Servlet-фильтров, которая стоит перед DispatcherServlet.
>
> **Три понятия:** идентификация (кто ты?), аутентификация (докажи), авторизация (что тебе можно).
>
> **Поток аутентификации:** POST /login → `UsernamePasswordAuthenticationFilter` создаёт токен → `AuthenticationManager` (реализация `ProviderManager`) обходит провайдеры → `DaoAuthenticationProvider` вызывает `UserDetailsService.loadUserByUsername` → загружает `UserDetails` → `PasswordEncoder.matches` проверяет пароль → при успехе кладёт `Authentication` в `SecurityContextHolder`.
>
> **SecurityContextHolder** хранит `Authentication` на уровне потока (ThreadLocal): `getPrincipal()` — кто, `getAuthorities()` — роли.
>
> **Конфигурация:** `SecurityFilterChain` через `HttpSecurity` — указываем какие URL требуют аутентификации, какие роли.
>
> **UserDetailsService** — главная точка кастомизации: реализуем `loadUserByUsername` — идём в БД, возвращаем `UserDetails` с ролями.
>
> **BCryptPasswordEncoder** — обязательно для паролей: встроенная соль, медленный алгоритм против brute-force."

## Шпаргалка

| Компонент | Роль | Ключевое |
|-----------|------|---------|
| **SecurityFilterChain** | Цепочка фильтров | Стоит до DispatcherServlet |
| **AuthenticationManager** | Координирует провайдеры | Реализация: ProviderManager |
| **DaoAuthenticationProvider** | Проверяет логин/пароль | Вызывает UserDetailsService |
| **UserDetailsService** | Загрузить пользователя из БД | loadUserByUsername() |
| **UserDetails** | Данные пользователя | username, password, authorities |
| **PasswordEncoder** | Проверить/закодировать пароль | BCryptPasswordEncoder |
| **SecurityContextHolder** | Хранит текущего пользователя | ThreadLocal, Authentication |
| **Authentication** | Кто аутентифицирован | principal + authorities |
| **@PreAuthorize** | Метод-уровневый контроль | SpEL, hasRole/hasAuthority |
| **401** | Не аутентифицирован | Нет токена/сессии |
| **403** | Нет прав | Аутентифицирован, но forbidden |

**Связи:**
- [[Spring Core IoC DI]]
- [[Spring Boot]]
- [[Хранение паролей хеширование шифрование]]
- [[Spring MVC REST (Controller vs RestController)]]
