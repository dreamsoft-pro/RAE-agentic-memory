<?php

namespace DreamSoft\Libs\LabelImposition\Requests;

use InvalidArgumentException;

class CreateLabelImpositionRequest implements RequestInterface
{
    private array $params;

    public function __construct(array $params)
    {
        $this->params = $params;
        try {
            $this->validate();
        } catch (InvalidArgumentException $e) {
            echo json_encode(['error' => $e->getMessage()], JSON_THROW_ON_ERROR);
            exit;
        }
    }

    public function validate(): bool
    {
        if (!isset($this->params['labelUrl'])) {
            throw new InvalidArgumentException('labelUrl is required');
        }

        if (!filter_var($this->params['labelUrl'], FILTER_VALIDATE_URL)) {
            throw new InvalidArgumentException('labelUrl is not a valid URL');
        }

        if (!isset($this->params['numberOfRows'])) {
            throw new InvalidArgumentException('numberOfRows is required');
        }

        if (!is_numeric($this->params['numberOfRows'])) {
            throw new InvalidArgumentException('numberOfRows must be a number');
        }

        if (isset($this->barcodes)) {
            foreach ($this->barcodes as $barcode) {
                if (!isset($barcode['data'])) {
                    throw new InvalidArgumentException('Barcode data is required');
                }

                if (!isset($barcode['positionX']) || $barcode['positionX'] === '') {
                    throw new InvalidArgumentException('Barcode position X is required');
                }

                if (!isset($barcode['positionY']) || $barcode['positionY'] === '') {
                    throw new InvalidArgumentException('Barcode position Y is required');
                }

                if (!isset($barcode['width']) || $barcode['width'] === '') {
                    throw new InvalidArgumentException('Barcode width is required');
                }

                if (!isset($barcode['height']) || $barcode['height'] === '') {
                    throw new InvalidArgumentException('Barcode height is required');
                }

                if ((float)$barcode['positionY'] > 0 && (float)$barcode['positionX'] > 0) {
                    throw new InvalidArgumentException('One of the barcode positions must be 0');
                }
            }
        }

        if (isset($this->qrcodes)) {
            foreach ($this->qrcodes as $qrcode) {
                if (!isset($qrcode['data'])) {
                    throw new InvalidArgumentException('QR code data is required');
                }

                if (!isset($qrcode['positionX']) || $qrcode['positionX'] === '') {
                    throw new InvalidArgumentException('QR code position X is required');
                }

                if (!isset($qrcode['positionY']) || $qrcode['positionY'] === '') {
                    throw new InvalidArgumentException('QR code position Y is required');
                }

                if (!isset($qrcode['height']) || $qrcode['height'] === '') {
                    throw new InvalidArgumentException('QR code size is required');
                }

                if ((float)$qrcode['positionY'] > 0 && (float)$qrcode['positionX'] > 0) {
                    throw new InvalidArgumentException('One of the QR code positions must be 0');
                }
            }
        }

        if (isset($this->photoCells)) {
            foreach ($this->photoCells as $photoCell) {
                if (!isset($photoCell['positionX']) || $photoCell['positionX'] === '') {
                    throw new InvalidArgumentException('Photocell position X is required');
                }

                if (!isset($photoCell['positionY']) || $photoCell['positionY'] === '') {
                    throw new InvalidArgumentException('Photocell position Y is required');
                }

                if (!isset($photoCell['width']) || $photoCell['width'] === '') {
                    throw new InvalidArgumentException('Photocell width is required');
                }

                if (!isset($photoCell['height']) || $photoCell['height'] === '') {
                    throw new InvalidArgumentException('Photocell height is required');
                }

                if ((float)$photoCell['positionY'] > 0 && (float)$photoCell['positionX'] > 0) {
                    throw new InvalidArgumentException('One of the photocell positions must be 0');
                }
            }
        }

        return true;
    }

    public function getParams(): array
    {
        return $this->params;
    }

    public function getParam(string $name, $default = null)
    {
        return $this->params[$name] ?? $default;
    }
}
