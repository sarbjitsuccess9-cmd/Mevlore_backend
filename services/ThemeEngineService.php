<?php
declare(strict_types=1);

require_once dirname(__DIR__) . '/includes/db.php';
require_once dirname(__DIR__) . '/includes/response.php';

/**
 * Dynamic Fashion Worlds Theme, Occasion, Campaign, Vector Asset, World Map & Offer Resolver.
 */
final class MelvoreThemeEngineService
{
    public static function computeConfigVersion(PDO $pdo): string
    {
        $parts = ['v2'];
        foreach (['app_style_worlds', 'app_campaigns', 'app_occasions', 'app_smart_offers', 'app_world_assets', 'app_brand_origins'] as $tbl) {
            if (MelvoreDB::tableExists($tbl)) {
                $cnt = (int)$pdo->query("SELECT COUNT(*) FROM `{$tbl}`")->fetchColumn();
                $parts[] = $tbl . ':' . $cnt;
            }
        }
        return substr(hash('sha256', implode('|', $parts)), 0, 16);
    }

    public static function loadDefaultTheme(): array
    {
        return [
            'theme_key' => 'melvore_default',
            'name' => 'Melvore Storefront',
            'mode' => 'light',
            'background_color' => '#FFFFFF',
            'surface_color' => '#F7F7FA',
            'surface_elevated' => '#EFEFF5',
            'primary_color' => '#09090B',
            'accent_color' => '#3B82F6',
            'secondary_accent' => '#9CA3AF',
            'text_primary' => '#09090B',
            'text_secondary' => '#52525B',
            'border_color' => '#E4E4E7',
            'font_style' => 'editorial_sans',
            'button_style' => 'sharp_minimal',
            'card_radius_dp' => 14,
            'border_width_dp' => 1,
            'ambient_preset' => 'none',
            'audio_track_key' => 'none',
            'motion_intensity' => 'subtle',
        ];
    }

    public static function formatWorldTheme(array $row): array
    {
        $cfg = [];
        if (!empty($row['theme_config'])) {
            $decoded = is_string($row['theme_config']) ? json_decode($row['theme_config'], true) : $row['theme_config'];
            if (is_array($decoded)) {
                $cfg = $decoded;
            }
        }
        $slug = (string)($row['slug'] ?? '');
        $bg = (string)($row['background_color'] ?? ($cfg['background_color'] ?? '#0B0B10'));
        $isDark = self::isDarkHex($bg);

        return [
            'style_world_id' => (int)($row['style_world_id'] ?? ($row['id'] ?? 0)),
            'slug' => $slug,
            'name' => (string)($row['name'] ?? ''),
            'tagline' => (string)($row['tagline'] ?? ''),
            'description' => (string)($row['description'] ?? ''),
            'theme_key' => (string)($row['theme_key'] ?? ($cfg['theme_key'] ?? $slug)),
            'mode' => (string)($cfg['mode'] ?? ($isDark ? 'dark' : 'light')),
            'animation_key' => (string)($row['animation_key'] ?? 'smooth_reveal'),
            'font_style' => (string)($row['font_style'] ?? 'editorial_serif'),
            'button_style' => (string)($cfg['button_style'] ?? ($row['button_style'] ?? 'editorial_pill')),
            'card_radius_dp' => (int)($cfg['card_radius_dp'] ?? ($row['card_radius_dp'] ?? 16)),
            'border_width_dp' => (int)($cfg['border_width_dp'] ?? 1),
            'primary_color' => (string)($row['primary_color'] ?? '#FFFFFF'),
            'accent_color' => (string)($row['accent_color'] ?? '#D4AF37'),
            'secondary_accent' => (string)($cfg['secondary_accent'] ?? '#9CA3AF'),
            'background_color' => $bg,
            'surface_color' => (string)($cfg['surface_color'] ?? ($isDark ? '#14141D' : '#F8F7FA')),
            'surface_elevated' => (string)($cfg['surface_elevated'] ?? ($isDark ? '#1E1E2B' : '#FFFFFF')),
            'text_primary' => (string)($cfg['text_primary'] ?? ($isDark ? '#FFFFFF' : '#121216')),
            'text_secondary' => (string)($cfg['text_secondary'] ?? ($isDark ? '#D4D4D8' : '#52525B')),
            'border_color' => (string)($cfg['border_color'] ?? ($isDark ? '#2E2E3E' : '#E5E7EB')),
            'ambient_preset' => (string)($row['ambient_preset'] ?? ($cfg['ambient_preset'] ?? $slug)),
            'audio_track_key' => (string)($row['audio_track_key'] ?? ($cfg['audio_track_key'] ?? $slug)),
            'sfx_profile' => (string)($cfg['sfx_profile'] ?? $slug),
            'hero_layout' => (string)($cfg['hero_layout'] ?? 'asymmetrical_split'),
            'cover_image_url' => MelvoreResponse::mediaUrl($row['cover_image_url'] ?? ($row['hero_image_url'] ?? null)),
            'mobile_image_url' => MelvoreResponse::mediaUrl($row['mobile_image_url'] ?? ($row['cover_image_url'] ?? null)),
            'video_url' => MelvoreResponse::mediaUrl($row['video_url'] ?? null),
            'display_order' => (int)($row['display_order'] ?? 0),
            'version_tag' => (string)($row['version_tag'] ?? '1.0'),
            'theme_config' => $cfg,
        ];
    }

    public static function fetchActiveOccasions(PDO $pdo, string $country = 'India', string $state = '', string $city = ''): array
    {
        if (!MelvoreDB::tableExists('app_occasions')) {
            return [];
        }
        $stmt = $pdo->query(
            'SELECT * FROM app_occasions
             WHERE is_active = 1
               AND (start_date IS NULL OR start_date <= NOW())
               AND (end_date IS NULL OR end_date >= NOW())
             ORDER BY priority DESC, occasion_id ASC'
        );
        $list = [];
        foreach ($stmt->fetchAll() as $row) {
            $rCountry = trim((string)($row['region_country'] ?? ''));
            $rState = trim((string)($row['region_state'] ?? ''));
            $rCity = trim((string)($row['region_city'] ?? ''));
            if ($rCountry !== '' && strcasecmp($rCountry, $country) !== 0 && strcasecmp($rCountry, 'ALL') !== 0) {
                continue;
            }
            if ($rState !== '' && $state !== '' && strcasecmp($rState, $state) !== 0) {
                continue;
            }
            if ($rCity !== '' && $city !== '' && strcasecmp($rCity, $city) !== 0) {
                continue;
            }
            $cfg = [];
            if (!empty($row['theme_config'])) {
                $decoded = is_string($row['theme_config']) ? json_decode($row['theme_config'], true) : $row['theme_config'];
                if (is_array($decoded)) {
                    $cfg = $decoded;
                }
            }
            $list[] = [
                'occasion_id' => (int)$row['occasion_id'],
                'slug' => (string)$row['slug'],
                'name' => (string)$row['name'],
                'eyebrow' => (string)($row['eyebrow'] ?? ''),
                'headline' => (string)($row['headline'] ?? ''),
                'subtitle' => (string)($row['subtitle'] ?? ''),
                'occasion_type' => (string)($row['occasion_type'] ?? 'festival'),
                'motif_key' => (string)($row['motif_key'] ?? 'confetti'),
                'primary_color' => (string)($row['primary_color'] ?? '#D4AF37'),
                'accent_color' => (string)($row['accent_color'] ?? '#FFFFFF'),
                'background_color' => (string)($row['background_color'] ?? '#140F1C'),
                'font_style' => (string)($row['font_style'] ?? 'editorial_serif'),
                'audio_track_key' => (string)($row['audio_track_key'] ?? 'festive'),
                'cta_text' => (string)($row['cta_text'] ?? 'Shop Edit'),
                'cta_collection_slug' => (string)($row['cta_collection_slug'] ?? ''),
                'banner_image_url' => MelvoreResponse::mediaUrl($row['banner_image_url'] ?? null),
                'priority' => (int)($row['priority'] ?? 0),
                'start_date' => $row['start_date'] ?? null,
                'end_date' => $row['end_date'] ?? null,
                'theme_config' => $cfg,
            ];
        }
        return $list;
    }

    public static function fetchWorldAssets(PDO $pdo): array
    {
        if (!MelvoreDB::tableExists('app_world_assets')) {
            return [];
        }
        $stmt = $pdo->query(
            'SELECT * FROM app_world_assets
             WHERE is_active = 1
             ORDER BY world_slug ASC, display_order ASC, asset_id ASC'
        );
        $assets = [];
        foreach ($stmt->fetchAll() as $row) {
            $meta = [];
            if (!empty($row['metadata_json'])) {
                $decoded = is_string($row['metadata_json']) ? json_decode($row['metadata_json'], true) : $row['metadata_json'];
                if (is_array($decoded)) {
                    $meta = $decoded;
                }
            }
            $assets[] = [
                'asset_id' => (int)$row['asset_id'],
                'asset_key' => (string)$row['asset_key'],
                'world_slug' => (string)$row['world_slug'],
                'occasion_slug' => $row['occasion_slug'] ?? null,
                'vector_type' => (string)$row['vector_type'],
                'layer_role' => (string)($row['layer_role'] ?? 'ambient_floating'),
                'primary_hex' => (string)($row['primary_hex'] ?? '#FFFFFF'),
                'secondary_hex' => (string)($row['secondary_hex'] ?? '#D4AF37'),
                'opacity' => (float)($row['opacity'] ?? 0.35),
                'motion_pattern' => (string)($row['motion_pattern'] ?? 'float_drift'),
                'image_url' => MelvoreResponse::mediaUrl($row['image_url'] ?? null),
                'metadata' => $meta,
            ];
        }
        return $assets;
    }

    public static function fetchWorldMapOrigins(PDO $pdo): array
    {
        $pins = [];
        if (MelvoreDB::tableExists('app_brand_origins')) {
            $hasProfiles = MelvoreDB::tableExists('app_brand_profiles');
            $sql = "SELECT o.*, b.name AS brand_name, b.slug AS brand_slug, b.logo AS brand_logo, b.description AS brand_description,
                           " . ($hasProfiles ? "bp.tagline AS brand_tagline, bp.story AS brand_story, bp.editorial_cover_url" : "NULL AS brand_tagline, NULL AS brand_story, NULL AS editorial_cover_url") . ",
                           (SELECT COUNT(*) FROM products p WHERE p.brand_id = b.brand_id AND p.is_active = 1) AS product_count
                    FROM app_brand_origins o
                    INNER JOIN brands b ON b.brand_id = o.brand_id AND b.status = 'active'
                    " . ($hasProfiles ? "LEFT JOIN app_brand_profiles bp ON bp.brand_id = b.brand_id" : "") . "
                    WHERE o.is_active = 1 AND o.is_verified = 1
                    ORDER BY o.display_order ASC, o.origin_id ASC";
            foreach ($pdo->query($sql)->fetchAll() as $row) {
                $pins[] = [
                    'origin_id' => (int)$row['origin_id'],
                    'brand_id' => (int)$row['brand_id'],
                    'brand_name' => (string)$row['brand_name'],
                    'brand_slug' => (string)$row['brand_slug'],
                    'brand_logo' => MelvoreResponse::mediaUrl($row['brand_logo'] ?? null),
                    'cover_image_url' => MelvoreResponse::mediaUrl($row['editorial_cover_url'] ?? null),
                    'tagline' => (string)($row['brand_tagline'] ?? ''),
                    'story' => (string)($row['origin_story'] ?? ($row['brand_story'] ?? ($row['brand_description'] ?? ''))),
                    'city' => (string)$row['city'],
                    'country' => (string)$row['country'],
                    'country_code' => (string)($row['country_code'] ?? ''),
                    'latitude' => (float)$row['latitude'],
                    'longitude' => (float)$row['longitude'],
                    'world_slug' => (string)($row['world_slug'] ?? ''),
                    'product_count' => (int)($row['product_count'] ?? 0),
                    'is_verified' => true,
                ];
            }
        }
        return $pins;
    }

    private static function isDarkHex(string $hex): bool
    {
        $clean = ltrim(trim($hex), '#');
        if (strlen($clean) === 8) {
            $clean = substr($clean, 2);
        }
        if (strlen($clean) !== 6 || !ctype_xdigit($clean)) {
            return true;
        }
        $r = hexdec(substr($clean, 0, 2));
        $g = hexdec(substr($clean, 2, 2));
        $b = hexdec(substr($clean, 4, 2));
        $luminance = (0.299 * $r + 0.587 * $g + 0.114 * $b) / 255.0;
        return $luminance < 0.52;
    }
}
