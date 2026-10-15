import type * as React from 'react';
/** O logo SIM (cruz, Maria e as letras SIM) em uma cor só: herda `color`. */
export interface LogoProps { size?: number; title?: string; className?: string }
export declare function Logo(props: LogoProps): React.ReactElement;
/** Chamada empilhada: `antes` e `depois` em ink, `destaque` em fogo. */
export interface ChamadaProps { antes?: React.ReactNode; destaque?: React.ReactNode; depois?: React.ReactNode; estilo?: 'cartaz' | 'titulo'; as?: 'h1' | 'h2' | 'h3' | 'p'; className?: string }
export declare function Chamada(props: ChamadaProps): React.ReactElement;
/** A linha de brasa com a faísca dourada no centro. */
export interface DivisorProps { largura?: string | number; className?: string }
export declare function Divisor(props: DivisorProps): React.ReactElement;
export interface BotaoProps extends React.ButtonHTMLAttributes<HTMLButtonElement> { variante?: 'fogo' | 'contorno' }
export declare function Botao(props: BotaoProps): React.ReactElement;
/** O endereço do site com o globo, como no rodapé dos posts. */
export interface SeloSiteProps { children?: React.ReactNode; href?: string; className?: string }
export declare function SeloSite(props: SeloSiteProps): React.ReactElement;
/** Post 4:5 completo: fogo nos cantos, chamada, divisor, texto, site e logo. */
export interface PostProps { selo?: string; antes?: React.ReactNode; destaque?: React.ReactNode; depois?: React.ReactNode; estilo?: 'cartaz' | 'titulo'; site?: string | false; children?: React.ReactNode; className?: string }
export declare function Post(props: PostProps): React.ReactElement;
declare global { interface Window { DigaSim: { Logo: typeof Logo; Chamada: typeof Chamada; Divisor: typeof Divisor; Botao: typeof Botao; SeloSite: typeof SeloSite; Post: typeof Post } } }
