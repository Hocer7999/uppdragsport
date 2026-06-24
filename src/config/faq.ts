export interface FAQItem {
    question: string;
    answer: string;
}

export const defaultFaqs: FAQItem[] = [
    {
        question: "Hur lång är bindningstiden?",
        answer:
            "Vi har ingen bindningstid på våra standardpaket. Du kan när som helst uppgradera, nedgradera eller avsluta din tjänst.",
    },
    {
        question: "Kan jag byta paket senare?",
        answer:
            "Ja, absolut! Du kan enkelt byta paket via din inloggning när dina behov förändras.",
    },
    {
        question: "Ingår support i alla paket?",
        answer:
            "Ja, vi erbjuder support för alla våra kunder. Nivån på supporten (t.ex. svarstider) kan variera beroende på vilket paket du väljer.",
    },
    {
        question: "Erbjuder ni fakturabetalning?",
        answer:
            "Ja, för företagskunder erbjuder vi fakturabetalning med 30 dagars betalningsvillkor. Vi accepterar även kortbetalning.",
    },
];
