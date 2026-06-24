// =====================================================================
// SECTION REGISTRY
// ---------------------------------------------------------------------
// A central map from section "type"-strings to their Astro components.
// Pages declare what they show via src/config/pages.ts as an array of
// SectionConfig items; SectionRenderer.astro looks each one up here and
// passes through props. This lets you compose pages from data instead of
// from imports, and switch site personalities (service / content /
// directory) by swapping the array.
// =====================================================================

import Hero from "../components/sections/Hero.astro";
import HeroVideo from "../components/sections/HeroVideo.astro";
import HeroSearch from "../components/sections/HeroSearch.astro";
import HeroWithForm from "../components/sections/HeroWithForm.astro";
import HeroCentered from "../components/sections/HeroCentered.astro";
import HeroSubpage from "../components/sections/HeroSubpage.astro";
import Services from "../components/sections/Services.astro";
import Features from "../components/sections/Features.astro";
import InfoCards from "../components/sections/InfoCards.astro";
import Stats from "../components/sections/Stats.astro";
import StatsAlt from "../components/sections/StatsAlt.astro";
import Pricing from "../components/sections/Pricing.astro";
import PricingCards from "../components/sections/PricingCards.astro";
import Steps from "../components/sections/Steps.astro";
import CTA from "../components/sections/CTA.astro";
import ContentBlock from "../components/sections/ContentBlock.astro";
import FAQ from "../components/sections/FAQ.astro";
import FAQWithSidebar from "../components/sections/FAQWithSidebar.astro";
import Contact from "../components/sections/Contact.astro";
import MultiStepForm from "../components/sections/MultiStepForm.astro";
import Kommun from "../components/sections/Kommun.astro";
import GraphSection from "../components/sections/GraphSection.astro";
import Articles from "../components/sections/Articles.astro";
import ArticleList from "../components/sections/ArticleList.astro";
import CategoryGrid from "../components/sections/CategoryGrid.astro";
import AuthorList from "../components/sections/AuthorList.astro";
import Newsletter from "../components/sections/Newsletter.astro";
import RelatedPosts from "../components/sections/RelatedPosts.astro";
import EditorialQuote from "../components/sections/EditorialQuote.astro";
import HeroStadium from "../components/sections/HeroStadium.astro";
import ScoreTicker from "../components/sections/ScoreTicker.astro";
import NewsRail from "../components/sections/NewsRail.astro";
import MomentsFilmstrip from "../components/sections/MomentsFilmstrip.astro";
import NewsPortal from "../components/sections/NewsPortal.astro";
import AdBanner from "../components/sections/AdBanner.astro";
import StandingsTable from "../components/sections/StandingsTable.astro";
import TopBreakingBar from "../components/sections/TopBreakingBar.astro";
import MatchCenter from "../components/sections/MatchCenter.astro";
import LeagueTables from "../components/sections/LeagueTables.astro";
import LatestWire from "../components/sections/LatestWire.astro";

export const sectionRegistry = {
    Hero,
    HeroVideo,
    HeroSearch,
    HeroWithForm,
    HeroCentered,
    HeroSubpage,
    Services,
    Features,
    InfoCards,
    Stats,
    StatsAlt,
    Pricing,
    PricingCards,
    Steps,
    CTA,
    ContentBlock,
    FAQ,
    FAQWithSidebar,
    Contact,
    MultiStepForm,
    Kommun,
    GraphSection,
    Articles,
    ArticleList,
    CategoryGrid,
    AuthorList,
    Newsletter,
    RelatedPosts,
    EditorialQuote,
    HeroStadium,
    ScoreTicker,
    NewsRail,
    MomentsFilmstrip,
    NewsPortal,
    AdBanner,
    StandingsTable,
    TopBreakingBar,
    MatchCenter,
    LeagueTables,
    LatestWire,
} as const;

export type SectionType = keyof typeof sectionRegistry;

export interface SectionConfig {
    type: SectionType;
    props?: Record<string, unknown>;
}
